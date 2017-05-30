from functools import partial
from collections import ChainMap
from inspect import signature

from support import Reservoir, Valve


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
        double_star_wrap = None,
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
          )



    # sets the wrapped function as a method in Pipe
    setattr(cls, gener_name, wrapper)

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


def _assemble_args(function_pipe, iter_index, args, kargs, star_wrap, double_star_wrap):
  if star_wrap is not None and double_star_wrap is not None:
    raise ValueError('star_wrap and double_star_wrap cannot both not be None.')

  elif star_wrap is not None:
    wrap_val = star_wrap

    def wrap_func(func):
      def func_out(to_unpack):
        return func(*to_unpack)
      return func_out

  elif double_star_wrap is not None:
    wrap_val = double_star_wrap

    def wrap_func(func):
      def func_out(to_unpack):
        return func(**to_unpack)
      return func_out

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
      kargs = ChainMap(
          {wrap_val: wrap_func(kargs[wrap_val])},
          kargs
        )

  elif wrap_val is not None:
    raise TypeError(
        'wrap_val must be of type int or str, but not type ' + str(type(wrap_val))
      )

  args = args[:iter_index] + (function_pipe,) + args[iter_index:]

  return args, kargs



