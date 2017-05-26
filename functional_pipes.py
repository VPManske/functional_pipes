import types
from functools import partial

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
    >>> data_1 = 2, 1, 3
    >>> valve_1 = Valve(func=sorted, pass_args=(data_1,), pass_whole=True)
    >>> next(valve_1)
    [1, 2, 3]
    >>> next(valve_1)
    raises StopIteration

    >>> valve_2 = Valve(func=sorted, pass_args=(data_1,), pass_whole=False)
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
    >>> valve_1 = Valve(func=test_function, pass_args=(data_1,), pass_whole=True)
    >>> result_1 = next(valve_1)
    3
    >>> result_1 = next(valve_1)
    raises StopIteration
  '''

  def __init__(self, func, pass_args, pass_kargs=None, pass_whole=False):
    '''
    func - A function that should consume the whole iterable and return an object.
      If the returned object is iterable, Valve will pass one value of the object iterator
      at a time unless pass_whole is True.

    pass_args - Arguments that will be unloaded into func with the * operator like *pass_args
    pass_kargs - Keyed arguments that will be unloaded into func with the ** operator like **pass_kargs

    pass_whole - If true the whole value is passed instead of breaking it up into an iterable.
    '''
    self.func = func
    self.pass_args = pass_args
    self.pass_kargs = pass_kargs if pass_kargs else {}
    self.pass_whole = pass_whole

    self.call_function = True

    if not pass_whole:
      self.iterator = None

  def __iter__(self):
    return self

  def __next__(self):
    if self.pass_whole:
      if self.call_function:
        # Pass the whole object returned by self.func(*self.pass_args, **self.pass_kargs) on the first call
        self.call_function = False
        return self.func(*self.pass_args, **self.pass_kargs)

      # raise StopIteration on the second call and reset to call self.func(*self.pass_args, **self.pass_kargs) again
      self.call_function = True
      raise StopIteration

    else:
      if self.call_function:
        self.call_function = False

        returned = self.func(*self.pass_args, **self.pass_kargs)
        try:
          # self.func(*self.pass_args, **self.pass_kargs) may not return an iterator
          self.iterator = iter(returned)
        except TypeError:
          # create iterator from non iterator
          self.iterator = iter((returned,))

      try:
        return next(self.iterator)
      except StopIteration:
        # raise StopIteration on the second call and reset to call self.func(*self.pass_args, **self.pass_kargs) again
        self.call_function = True
        raise StopIteration


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
  def add_method(cls, gener, is_valve=False, iter_index=0, gener_name=None, no_over_write=True):
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
    '''
    if not gener_name:
      gener_name = gener.__name__

    if no_over_write and hasattr(cls, gener_name):
      raise AttributeError('Point class already has the gener ' + gener.__name__)

    '''
    Creates a wrapped generator that can be added to the class Pipe.
    The wrapper always puts the iterable in the correct location in the gener's arguments.

    gener - generator to be wrapped
    iter_index - the index of the arguments to pass the iterable
    is_valve - should be true if the gener is
    '''
    if is_valve:
      def wrapper(self, *args, **kargs):

        # arguments with the iterator in the proper location
        args_gener = args[:iter_index] + (self.function_pipe,) + args[iter_index:]

        if self.preloaded:
          '''
          If the Pipe is preloaded with data and a valve is added the Pipe will run the
          pre loaded iterator and return the value.
          '''
          to_return = gener(*args_gener, **kargs)

        else:
          to_return = Pipe(
              iterable_pre_load = self.preloaded,
              function_pipe = Valve(gener, args_gener, kargs),
              reservoir = self.reservoir,
              valve = True,
            )

        return to_return

    else:
      def wrapper(self, *args, **kargs):
        args = args[:iter_index] + (self.function_pipe,) + args[iter_index:]
        return Pipe(
            iterable_pre_load = self.preloaded,
            function_pipe = gener(*args, **kargs),
            reservoir = self.reservoir,
            valve = False
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



# def consume_all(iterator)
# # feed the entire iterator into a zero-length deque
# deque(iterator, maxlen=0)


methods = (
  (enumerate, 0),
  (min, 0),
  (filter, 1),
)


# enumerate(iterable, start=0)
# min(iterable, *[, key, default])
# filter(function, iterable)






import unittest


class TestPipe(unittest.TestCase):
  # def test_call_iter_next(self):
  #   '''
  #   test iter, next, call.
  #   No extra methods added.
  #   '''
  #   data_1 = 1, 2, 3, 4
  #   data_2 = 5, 6, 7, 8

  #   pipe_1 = Pipe()
  #   pipe_1(data_1)
  #   self.assertEqual(tuple(pipe_1), data_1)
  #   self.assertEqual(tuple(pipe_1(data_2)), data_2)

  #   pipe_1(data_1)
  #   for p, d in zip(pipe_1, data_1):
  #     self.assertTrue(p is d)
  #   for p, d in zip(pipe_1(data_2), data_2):
  #     self.assertTrue(p is d)

  #   # preloaded iterable
  #   pipe3 = Pipe(data_1)
  #   self.assertEqual(tuple(pipe3), data_1)
  #   with self.assertRaises(StopIteration):
  #     next(pipe3)
  #   self.assertEqual(tuple(pipe3(data_2)), data_2)

  # def test_add_method(self):

  #   # enumerate
  #   Pipe.add_method(enumerate)
  #   self.assertTrue(hasattr(Pipe, 'enumerate'))
  #   self.assertTrue(isinstance(Pipe.enumerate, types.FunctionType))
  #   self.assertTrue(isinstance(Pipe().enumerate, types.MethodType))
  #   with self.assertRaises(AttributeError):
  #     Pipe.add_method(enumerate)
  #   with self.assertRaises(AttributeError):
  #     Pipe.add_method(map, gener_name='enumerate')

  #   # no_over_write is False
  #   Pipe.add_method(enumerate, no_over_write=False)
  #   self.assertTrue(hasattr(Pipe, 'enumerate'))
  #   self.assertTrue(isinstance(Pipe.enumerate, types.FunctionType))
  #   self.assertTrue(isinstance(Pipe().enumerate, types.MethodType))

  #   Pipe.add_method(enumerate, 'enumerate', no_over_write=False)
  #   self.assertTrue(hasattr(Pipe, 'enumerate'))
  #   self.assertTrue(isinstance(Pipe.enumerate, types.FunctionType))
  #   self.assertTrue(isinstance(Pipe().enumerate, types.MethodType))

  #   # test added method
  #   data_1 = 1, 2, 3, 4

  #   self.assertEqual(
  #       tuple(Pipe(data_1).enumerate()),
  #       tuple(enumerate(data_1))
  #     )
  #   self.assertEqual(
  #       tuple(Pipe(data_1).enumerate(2)),
  #       tuple(enumerate(data_1, 2))
  #     )
  #   self.assertEqual(
  #       tuple(Pipe(data_1).enumerate(start=2)),
  #       tuple(enumerate(data_1, start=2))
  #     )

  #   # clean up methods
  #   delattr(Pipe, 'enumerate')

  # def test_add_map_method(self):
  #   data_1 = 1, 2, 7, 9
  #   data_1_squared = tuple(d**2 for d in data_1)

  #   Pipe.add_map_method(lambda a: a**2, 'square')

  #   self.assertEqual(tuple(Pipe(data_1).square()), data_1_squared)

  #   # clean up methods
  #   delattr(Pipe, 'square')


  # def test_pipe_creation_single_flow(self):
  #   '''
  #   Extending a Pipe with a
  #   '''
  #   data_1 = 1, 2, 3, 4


  def test_pipe_valve(self):
    data_1 = 4, 2, 8, -5
    data_1_min = min(data_1)

    # test method that directly passes the data through
    Pipe.add_map_method(lambda val: val, 'pass_through')
    # min
    Pipe.add_method(min, is_valve=True)

    # '''
    # The Pipe has been preloaded and a valve has been added to the pipe.
    # When the preloaded and a valve is added the reservoir should be drained
    # by the pipe into the valve function and the result should be returned.
    # '''
    # self.assertEqual(
    #     Pipe(data_1).min(),
    #     data_1_min
    #   )
    # self.assertEqual(
    #     Pipe(data_1).pass_through().min(),
    #     data_1_min
    #   )

    '''
    Pipe has not been preloaded and a Pipe should be returned.
    '''
    pipe_1 = Pipe().min()
    self.assertEqual(pipe_1(data_1), data_1_min)
    self.assertEqual(pipe_1(data_1), data_1_min)  # not a repeat

    pipe_2 = Pipe().pass_through().min()
    self.assertEqual(pipe_1(data_1), data_1_min)

    pip_3 = Pipe().min().pass_through()
    self.assertEqual(next(pip_3(data_1)), data_1_min)

    pip_4 = Pipe().min().min()
    self.assertEqual(pipe_1(data_1), data_1_min)

    pipe_5 = pipe_1.pass_through()
    self.assertEqual(
        next(pipe_5(data_1)),
        next(pip_3(data1))
      )

    pipe_6 = pipe_1.min()
    self.assertEqual(
        next(pipe_6(data_1)),
        next(pip_4(data1))
      )

    # clean up
    delattr(Pipe, 'pass_through')
    delattr(Pipe, 'min')


class TestValve(unittest.TestCase):
  def test_iterable_object(self):
    '''
    tests functions that return an iterable object
    using sorted because it returns an iterable object
    '''
    test_function = sorted

    data_1 = 2, 1, 3
    data_2 = 5, 2, 6, 7, 2, 4, 6

    '''
    pass_whole is True
    should pass the whole sorted list back
    '''
    valve_1 = Valve(func=test_function, pass_args=(data_1,), pass_whole=True)
    valve_2 = Valve(func=test_function, pass_args=(data_2,), pass_whole=True)
    result_1 = next(valve_1)
    result_2 = next(valve_2)
    self.assertEqual(result_1, sorted(data_1))
    self.assertEqual(result_2, sorted(data_2))
    self.assertTrue(isinstance(result_1, list))
    self.assertTrue(isinstance(result_2, list))

    with self.assertRaises(StopIteration):
      next(valve_1)
    with self.assertRaises(StopIteration):
      next(valve_2)

    # test reuse with Reservoir
    resv_3 = Reservoir(data_1)
    valve_3 = Valve(func=test_function, pass_args=(resv_3,), pass_whole=True)
    self.assertTrue(next(valve_3), sorted(data_1))
    with self.assertRaises(StopIteration):
      next(valve_3)

    resv_3(data_2)
    self.assertTrue(next(valve_3), sorted(data_2))

    # pass_whole is False
    valve_4 = Valve(func=test_function, pass_args=(data_1,), pass_whole=False)
    self.assertTrue(next(valve_4) is sorted(data_1)[0])
    for f, d in zip(valve_4, sorted(data_1)[1:]):
      self.assertTrue(f is d)

    # pass in a karg with pass_kargs
    valve_5 = Valve(
        func=test_function,
        pass_args=(data_1,),
        pass_kargs=dict(reverse=True),
        pass_whole=True
      )
    result_5 = next(valve_5)
    self.assertEqual(result_5, sorted(data_1, reverse=True))
    self.assertTrue(isinstance(result_5, list))
    with self.assertRaises(StopIteration):
      next(valve_5)

  def test_non_iterable_object(self):
    '''
    tests functions that return a non iterable object
    using max because it returns a non iterable object
    '''
    test_function = max

    data_1 = 2, 1, 3
    max_1 = test_function(data_1)
    data_2 = 5, 2, 6, 7, 2, 4, 6
    max_2 = test_function(data_2)

    # pass_whole is true
    valve_1 = Valve(func=test_function, pass_args=(data_1,), pass_whole=True)
    result_1 = next(valve_1)
    self.assertTrue(result_1 is max_1)
    with self.assertRaises(StopIteration):
      next(valve_1)

    # pass_whole is False
    valve_2 = Valve(func=test_function, pass_args=(data_1,), pass_whole=False)
    result_1 = next(valve_2)
    self.assertTrue(result_1 is max_1)
    with self.assertRaises(StopIteration):
      next(valve_2)


class TestReservoir(unittest.TestCase):
  def test_init(self):
    Reservoir()

    data_1 = 1, 2, 3, 4
    sp1 = Reservoir(data_1)
    self.assertEqual(tuple(sp1.iterator), data_1)

    sp2 = Reservoir(data_1)
    self.assertTrue(sp1 is not sp2)

  def test_iter_next_call(self):
    # test iter and next
    sp1 = Reservoir()

    with self.assertRaises(StopIteration):
      next(sp1)

    data_1 = tuple(range(10))
    sp1(range(10))

    for s, d in zip(sp1, data_1):
      self.assertEqual(s, d)


    # test call
    sp2 = Reservoir()

    with self.assertRaises(TypeError):
      next(sp2.iterator)

    # first fill
    data_1 = 1, 2, 3
    sp2(data_1)
    self.assertEqual(tuple(sp2), data_1)

    # second fill
    data_2 = 4, 5, 6
    sp2(data_2)
    self.assertEqual(tuple(sp2), data_2)

    # call when reservoir not yet empty
    sp2(data_1)
    with self.assertRaises(ValueError):
      sp2(data_1)


if __name__ == '__main__':
  unittest.main()
