from functools import partial
from collections import ChainMap
from inspect import signature


class Pipe:
  def __init__(self, iterable_pre_load=None, function_pipe=None, reservoir=None, valve=False):
    # True if an iterable is data is preloaded into the pipe
    self.preloaded = bool(iterable_pre_load)

    # Iterable source for the Pipe
    self.reservoir = reservoir if reservoir else Reservoir(iterable_pre_load)

    # The chain of functions that data will be fed through.
    self.function_pipe = function_pipe if function_pipe else self.reservoir

    # True if the end of the pipe is a valve function else False
    self.valve = valve

  def __call__(self, iterable):
    self.reservoir(iterable)
    if self.valve:
      return next(self.function_pipe)

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
      ):
    '''
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

    if no_over_write and hasattr(cls, gener_name):
      raise AttributeError('Point class already has the gener ' + gener_name)

    # sets the wrapped function as a method in Pipe
    setattr(cls, gener_name,
      _create_wrapper(
          gener = gener,
          iter_index = iter_index,
          is_valve = is_valve,
          empty_error = empty_error,
          star_wrap = star_wrap,
        ))

    # if star_wrap is not None:
    #   setattr(cls, 's_' + gener_name,
    #     _create_wrapper(
    #         gener = gener,
    #         iter_index = iter_index,
    #         is_valve = is_valve,
    #         empty_error = empty_error,
    #         star_wrap = star_wrap,
    #       ))

  @classmethod
  def add_map_method(cls, func, func_name=None, no_over_write=True):
    '''
    Similar to Pipe.add_method but takes a function not a generator.
    The function becomes the mapping function.

    func - must be a function.
      if a lambda function func_name must be a string for the method name.
    '''
    cls.add_method(
        gener = partial(map, func),
        gener_name = func_name if func_name else func.__name__,
        no_over_write = no_over_write,
      )


def star_arguments(func):
  def func_out(to_unpack):
    return func(*to_unpack)
  return func_out


def _assemble_args(function_pipe, iter_index, args, kargs, star_wrap):
  # arguments with the iterator in the proper location
  if isinstance(star_wrap, int):
    # this could be functionalized
    print('star_wrap', star_wrap)
    print('iter_index', iter_index)
    to_star = args[star_wrap] if star_wrap < iter_index else args[star_wrap - 1]
    star_function = (star_arguments(to_star)
                     if len(signature(to_star).parameters) > 1
                     else to_star)

    print('args1', args)
    split1 = args[:star_wrap if star_wrap < iter_index else star_wrap - 1]
    split2 = args[star_wrap+1:]
    print('split1', split1)
    print('split2', split2)
    args = (
            args[:star_wrap] +
            # (lambda to_unpack: args[star_wrap](*to_unpack),) +
            (star_function,) +
            args[star_wrap + 1:]
           )
    print('args2', args)
    split1 = args[:iter_index]
    split2 = args[iter_index:]
    print('split1', split1)
    print('split2', split2)
    args = args[:iter_index] + (function_pipe,) + args[iter_index:]

    print('args3', args)
    return args, kargs # FOR TESTING ONLY

  # elif isinstance(star_wrap, str):
  #   kargs = ChainMap(
  #       # {star_wrap: lambda to_unpack: kargs[star_wrap](*to_unpack)},
  #       {star_wrap: star_arguments(kargs[star_wrap])},
  #       kargs
  #     )

  elif star_wrap is not None:
    raise TypeError(
        'star_wrap must be of type int or str, but is type ' + str(type(star_wrap))
      )

  else:
    args = args[:iter_index] + (function_pipe,) + args[iter_index:]

  raise ValueError
  return args, kargs


def _create_wrapper(gener, iter_index, is_valve, empty_error, star_wrap):
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
                pass_args = args,
                pass_kargs = kargs,
                empty_error = empty_error,
              ),
            reservoir = self.reservoir,
            valve = True,
          )

      return to_return

  else:
    def wrapper(self, *args, **kargs):
      print('wrapper2')
      args, kargs = _assemble_args(
                function_pipe = self.function_pipe,
                iter_index = iter_index,
                args = args,
                kargs = kargs,
                star_wrap = star_wrap,
              )

      print('gener', gener)
      print('args', args)
      print('kargs', kargs)
      return Pipe(
          iterable_pre_load = self.preloaded,
          function_pipe = gener(*args, **kargs),
          reservoir = self.reservoir,
          valve = False,
        )

  return wrapper


class Reservoir:
  '''
  Single threaded iterator that gives a handle to the beginning of the function pipe.
  '''

  def __init__(self, iterable=None):
    '''
    iterable - preloads the instance with values to return when __next__ is called
    '''
    self.iterator = iter(iterable) if iterable else None

  def __call__(self, iterable):
    '''
    Reloads the instance with values.
    Checks if self is empty and raises an error if not empty.

    iterable - must be iterable
    '''
    if self.iterator:
      raise ValueError('{} is not empty.'.format(self))
    self.iterator = iter(iterable)

  def __iter__(self):
    return self

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

  def __init__(self, func, pass_args, pass_kargs=None, empty_error=None):
    '''
    func - A function that should consume the whole iterable and return an object.
      If the returned object is iterable, Valve will pass one value of the object iterator
      at a time.

    pass_args - Arguments that will be unloaded into func with the * operator like *pass_args
    pass_kargs - Keyed arguments that will be unloaded into func with the ** operator like **pass_kargs

    empty_error - error that is thrown if func recieves an empty iterator
    '''
    self.func = func
    self.pass_args = pass_args
    self.pass_kargs = pass_kargs if pass_kargs else {}
    self.empty_error = empty_error

    self.iterator = iter(())

  def __iter__(self):
    return self

  def __next__(self):
    try:
      to_return = next(self.iterator)
    except StopIteration:
      try:
        from_func = self.func(*self.pass_args, **self.pass_kargs)
      except self.empty_error:
        raise StopIteration

      try:
        # self.func(*self.pass_args, **self.pass_kargs) may not return an iterator
        self.iterator = iter(from_func)
        to_return = next(self.iterator)
      except TypeError:
        # create iterator from non iterator
        to_return = from_func

    return to_return
