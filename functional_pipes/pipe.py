from functools import partial
from collections import ChainMap, deque
from inspect import signature

from more_itertools import peekable, consume

from functional_pipes.bypass import Bypass, Drip, add_bypasses


class Pipe:
  def __init__(self,
        iterable_pre_load = None,
        function_pipe = None,
        reservoir = None,
        valve = False,
        enclosing_pipe = None,  # pipe that encloses the bypass pipe
      ):
    # True if an iterable is data is preloaded into the pipe
    self.preloaded = True if iterable_pre_load is not None else None

    # Iterable source for the Pipe
    self.reservoir = reservoir if reservoir else Reservoir(iterable_pre_load)

    # The chain of functions that data will be fed through.
    self.function_pipe = function_pipe if function_pipe else self.reservoir

    # True if the end of the pipe is a valve function else False
    self.valve = valve

    # the pipe that wraps this pipe and should be retruned when the wrap is over
    self.enclosing_pipe = enclosing_pipe

  def __call__(self, iterable):
    self.reservoir(iterable)
    if self.valve:
      return self.function_pipe.whole_return()

    return self

  def __iter__(self):
    return self

  def __next__(self):
    return next(self.function_pipe)

  @classmethod
  def add_method(
        cls,
        gener,
        is_valve = False,
        iter_index = 0,
        gener_name = None,
        no_over_write = True,
        empty_error = None,
        star_wrap = None,
        double_star_wrap = None,
      ):
    '''
    Used to add methods to the Pipe class.
    Returns the new method name.

    gener - generator to be added

    iter_index - index of the iterator argument for gener
      For enumerate(iterable, start=0) iter_index is 0
      For filter(function, iterable) iter_index is 1

    gener_name - Unnecessary if gener.__name__ is defined correctly.
      string that the gener will be called by.
      Has precedence over gener.__name__

    no_over_write - If True an AttributeError will be raised if there is already a method with
      the gener_name or gener.__name__. If False any method will be overwritten.

    empty_error - error that is thrown if gener recieves an empty iterator.
      Only applies if is_valve is True.

    star_wrap - int or str that specifies what argument to wrap with a star.
      Used so that functions can have multiple arguments.
      Also, this helps the user keep track what the passed objects are in each link.

      Ex with star_wrap:
        data = [(1, 2), (3, 4)]
        Pipe(data).filter(lambda x, y: x > y)
      Ex without star_wrap:
        Pipe(data).filter(lambda xy: xy[0] > xy[1])
    '''
    if not gener_name:
      gener_name = gener.__name__

    # if gener_name == 'min':
    #   raise ValueError('min')

    if no_over_write and hasattr(cls, gener_name):
      raise AttributeError('Pipe class already has the gener ' + gener_name)


    '''
    Creates a wrapped generator that can be added to the class Pipe.
    The wrapper always puts the iterable in the correct location in the gener's arguments.

    gener - generator to be wrapped
    iter_index - the index of the arguments to pass the iterable
    is_valve - should be true if the gener is
    '''
    if is_valve:
      def wrapper(self, *args, **kargs):

        args, kargs = _assemble_args(
            function_pipe = self.function_pipe,
            iter_index = iter_index,
            args = args,
            kargs = kargs,
            star_wrap = star_wrap,
            double_star_wrap = double_star_wrap,
          )

        if self.preloaded:
          '''
          If the Pipe is preloaded with data and a valve is added the Pipe will run the
          pre loaded iterator and return the value.
          '''
          to_return = gener(*args, **kargs)

        else:
          to_return = Pipe(
              iterable_pre_load = self.preloaded,
              function_pipe = Valve(
                  func = gener,
                  iterator = self.function_pipe,
                  pass_args = args,
                  pass_kargs = kargs,
                  empty_error = empty_error,
                ),
              reservoir = self.reservoir,
              valve = True,
              enclosing_pipe = self.enclosing_pipe,
            )

        return to_return

    else:
      def wrapper(self, *args, **kargs):
        args, kargs = _assemble_args(
                  function_pipe = self.function_pipe,
                  iter_index = iter_index,
                  args = args,
                  kargs = kargs,
                  star_wrap = star_wrap,
                  double_star_wrap = double_star_wrap,
                )

        return Pipe(
            iterable_pre_load = self.preloaded,
            function_pipe = gener(*args, **kargs),
            reservoir = self.reservoir,
            valve = False,
            enclosing_pipe = self.enclosing_pipe,
          )

    # sets the wrapped function as a method in Pipe
    setattr(cls, gener_name, wrapper)

    return gener_name

  @classmethod
  def add_map_method(cls, func, func_name=None, no_over_write=True):
    # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4

    '''
    Similar to Pipe.add_method but takes a function not a generator.
    The function becomes the mapping function.

    func - must be a function.
      if a lambda function func_name must be a string for the method name.
    func_name - the Pipe method name
      defaults to the func.__name__ string if not defined
    no_over_write - If True an AttributeError will be raised if there is already a method with
      the gener_name or gener.__name__. If False any method will be overwritten.
    '''
    def map_method_wrap(*args, **kargs):
      '''
      Allows methods to be passed to the function that map will call.
      '''
      iterator = args[0]
      args = args[1:]
      return map(lambda iter_obj: func(iter_obj, *args, **kargs), iterator)

    return cls.add_method(
        gener = map_method_wrap,
        gener_name = func_name if func_name else func.__name__,
        no_over_write = no_over_write,
      )

  @classmethod
  def add_key_map_method(cls, func, func_name=None, no_over_write=True):
    # https://github.com/BebeSparkelSparkel/functional_pipes/issues/6

    '''
    Similar to Pipe.add_map_method but returns a key and the function output
    instead of just mapping the function value.

    Example:
    >>> Pipe('1', '2').int_key().tuple()
    (('1', 1), ('2', 2))

    func - must be a function.
      if a lambda function func_name must be a string for the method name.
    func_name - the Pipe method name
      defaults to the func.__name__ string if not defined
    no_over_write - If True an AttributeError will be raised if there is already a method with
      the gener_name or gener.__name__. If False any method will be overwritten.
    '''
    return cls.add_map_method(
        func = lambda val: (val, func(val)),
        func_name = func_name,
        no_over_write = no_over_write,
      )

  def open_bypass(self):
    '''
    Opens a bypass Pipe that will take part of the output from the previous
    pipe section.
    Used multiple times by Pipe.add_bypass but assigned as a property with
    different names to show its relationship with its related closing bypass
    property method.
    '''
    return Pipe(
        reservoir = Drip(),
        enclosing_pipe = self,
      )

  @classmethod
  def add_bypass(cls, open_name, close_name, split, merge):
    '''
    Allows new bypass operations to be created that operates on part of the data
    created by the previous pipe segment.

    Example:
    Pipe.carry_key and Pipe.re_key are good examples of this. carry_key is a
    property method that just calls open_bypass and re_key is its paired method
    that will rekey the bypass pipe.
    >>> Pipe([(1, 2), (3, 4), (5, 6)]
    >>>   ).carry_key.map(lambda b: 2 * b  # map now only gets index 1 of the tuple elements
    >>>   ).filter(lambda b: b < 10  # filter also only gets the map modified (times 2) index 1 of the tuple elements
    >>>   ).re_key.list()  # re_key now merges the modified and filtered values back together and passes them to list
    [(1, 4), (3, 8)]
    '''
    setattr(cls, open_name, property(cls.open_bypass))  # bypass opener

    def close_bypass(self):
      enclosing_pipe = self.enclosing_pipe

      bpp = Bypass(
          bypass = self,
          iterable = enclosing_pipe,
          drip_handle = self.reservoir,
          split = split,
          merge = merge,
        )

      return Pipe(
          iterable_pre_load = enclosing_pipe.preloaded,
          function_pipe = bpp,
          reservoir = enclosing_pipe.reservoir,
        )

    setattr(cls, close_name, property(close_bypass))


'''
Addes all the bypasses defined in bypass.py
'''
add_bypasses(Pipe)


def _assemble_args(function_pipe, iter_index, args, kargs, star_wrap, double_star_wrap):
  '''
  Process all the arguments to pass into a function that is a method of Pipe.

  iter_index - the index of the iterator argument to be passed into the function.
    ars will be split and function_pipe will be inserted in between the splits
    and re-combined

  args - the indexed arguments that are to be pass into the function with the * operator

  kargs - the kargs that are to be passed into the functions with the ** operator

  star_wrap - a int, str, or None that specifies the argument that should be wrapped
    with the star operator.
    If an int then the argument in args at index star_wrap will be wrapped.
    If a str then the argument in kargs at key will be wrapped.
    If None then no arguments are wrapped.

  double_star_wrap - is the same as star_wrap but applies the ** operator
  '''
  if star_wrap is not None and double_star_wrap is not None:
    raise ValueError('star_wrap and double_star_wrap cannot both not be None.')

  elif star_wrap is not None:
    wrap_val = star_wrap

    def wrap_func(func):
      def func_out_single_star(to_unpack):
        return func(*to_unpack)
      return func_out_single_star

  elif double_star_wrap is not None:
    wrap_val = double_star_wrap

    def wrap_func(func):
      def func_out_double_star(to_unpack):
        return func(**to_unpack)
      return func_out_double_star

  else:
    wrap_val = None

  if isinstance(wrap_val, int):
    # this could be functionalized
    to_star = args[wrap_val] if wrap_val < iter_index else args[wrap_val - 1]
    star_function = (wrap_func(to_star)
                     if len(signature(to_star).parameters) > 1
                     else to_star)

    split_index = wrap_val if wrap_val < iter_index else wrap_val - 1
    args = args[:split_index] + (star_function,) + args[split_index + 1:]

  elif isinstance(wrap_val, str):
    if wrap_val in kargs.keys():
      to_star = kargs[wrap_val]
      star_function = (wrap_func(to_star)
                     if len(signature(to_star).parameters) > 1
                     else to_star)

      kargs = ChainMap(
          {wrap_val: star_function},
          kargs
        )

  elif wrap_val is not None:
    raise TypeError(
        'wrap_val must be of type int or str, but not type ' + str(type(wrap_val))
      )

  args = args[:iter_index] + (function_pipe,) + args[iter_index:]

  return args, kargs


class Reservoir:
  '''
  Single threaded iterator that gives a handle to the beginning of the function pipe.
  '''

  def __init__(self, iterable=None):
    '''
    iterable - preloads the instance with values to return when __next__ is called
    '''
    self.iterator = peekable(iterable) if iterable else None

  def __call__(self, iterable):
    '''
    Reloads the instance with values.
    Checks if self is empty and raises an error if not empty.

    Adds an extra check from Reservoir because

    iterable - must be iterable
    '''
    if self.iterator and self.iterator.peek(ReservoirEmpty) is not ReservoirEmpty:
      raise ValueError('{} is not empty.'.format(self))

    self.iterator = peekable(iterable)

  def __next__(self):
    '''
    Returns a value as long as there are loaded values.
    If there are no loaded values StopIteration is raised.
    '''
    try:
      return next(self.iterator)
    except StopIteration as err:
      self.iterator = None
      raise err
    except TypeError:
      raise StopIteration('Reservoir is empty.')

  def __iter__(self):
    return self


class ReservoirEmpty:
  '''
  Class to return if the peekable iterator is empty in Reservoir.__call__
  '''
  pass


class Valve:
  '''
  Transforms functions that accept iterators and returns a value into a generator.
  This allow functions that are not generators to be passed into a pipe.

  IMPROVEMENT:
  __next__ has a lot of dynamic checks if this could be doen in __init__ it would
    help the pipeline performance.

  Example with sorted:
    >>> valve_2 = Valve(func=sorted, pass_args=(data_1,)e)
    >>> next(valve_2)
    1
    >>> next(valve_2)
    2
    >>> next(valve_2)
    3
    >>> next(valve_2)
    raises StopIteration

  Example with max:
    >>> data_1 = 2, 1, 3
    >>> valve_1 = Valve(func=test_function, pass_args=(data_1,))
    >>> result_1 = next(valve_1)
    3
    >>> result_1 = next(valve_1)
    raises StopIteration
  '''

  def __init__(self, func, iterator, pass_args, pass_kargs=None, empty_error=None):
    '''
    func - A function that should consume the whole iterable and return an object.
      If the returned object is iterable, Valve will pass one value of the object iterator
      at a time.

    iterator - the iterator that is also contained in pass_args or pass_kargs.
      it is here so that it can be completely consumed if func does not completely
      consume it

    pass_args - Arguments that will be unloaded into func with the * operator like *pass_args
    pass_kargs - Keyed arguments that will be unloaded into func with the ** operator like **pass_kargs

    empty_error - error that is thrown if func recieves an empty iterator

    Important Note: The iterable that is passed in with pass_args or pass_kargs
      can be replenished with the function iter the values returnd by that iterable
      will continue to be passed in an infinate loop.
    '''
    self.func = func
    self.iterator = iterator
    self.pass_args = pass_args
    self.pass_kargs = pass_kargs if pass_kargs else {}
    self.empty_error = empty_error

    self.post_iterator = iter(())

  def __iter__(self):
    return self

  def __next__(self):
    try:
      to_return = next(self.post_iterator)
    except StopIteration:
      try:
        from_func = self.func(*self.pass_args, **self.pass_kargs)
        consume(self.iterator)
      except self.empty_error:
        raise StopIteration

      try:
        self.post_iterator = iter(from_func)
        to_return = next(self.post_iterator)
      except TypeError:
        # create iterator from non iterator
        to_return = from_func

    return to_return

  def whole_return(self):
    '''
    Returns the object created by the function and iterable.
    Used inplace of __next__ if the returned object should not be converted to an
    iterable.
    '''
    from_func = self.func(*self.pass_args, **self.pass_kargs)
    consume(self.iterator)
    return from_func
