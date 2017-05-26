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
    >>> f1 = Valve(func=sorted, pre_pipe=data_1, pass_whole=True)
    >>> next(f1)
    [1, 2, 3]
    >>> next(f1)
    raises StopIteration

    >>> f2 = Valve(func=sorted, pre_pipe=data_1, pass_whole=False)
    >>> next(f2)
    1
    >>> next(f2)
    2
    >>> next(f2)
    3
    >>> next(f2)
    raises StopIteration

  Example with max:
    >>> data_1 = 2, 1, 3
    >>> f1 = Valve(func=test_function, pre_pipe=data_1, pass_whole=True)
    >>> result_1 = next(f1)
    3
    >>> result_1 = next(f1)
    raises StopIteration
  '''

  def __init__(self, func, pre_pipe, pass_whole=False):
    '''
    func - A function that should consume the whole iterable and return an object.
      If the returned object is iterable, Valve will pass one value of the object iterator
      at a time unless pass_whole is True.

    pre_pipe - A generator that can be consumed. Will probably be the pipe that has already
      been constructed.

    pass_whole - If true the whole value is passed instead of breaking it up into an iterable.
    '''
    self.func = func
    self.pre_pipe = pre_pipe
    self.pass_whole = pass_whole

    self.call_function = True

    if not pass_whole:
      self.iterator = None

  def __iter__(self):
    return self

  def __next__(self):
    if self.pass_whole:
      if self.call_function:
        # Pass the whole object returned by self.func(self.pre_pipe) on the first call
        self.call_function = False
        return self.func(self.pre_pipe)

      # raise StopIteration on the second call and reset to call self.func(self.pre_pipe) again
      self.call_function = True
      raise StopIteration

    else:
      if self.call_function:
        self.call_function = False

        returned = self.func(self.pre_pipe)
        try:
          # self.func(self.pre_pipe) may not return an iterator
          self.iterator = iter(returned)
        except TypeError:
          # create iterator from non iterator
          self.iterator = iter((returned,))

      try:
        return next(self.iterator)
      except StopIteration:
        # raise StopIteration on the second call and reset to call self.func(self.pre_pipe) again
        self.call_function = True
        raise StopIteration


class Pipe:
  def __init__(self, iterable_pre_load=None, function_pipe=None, reservoir=None, valve=False):
    # True if an iterable is data is preloaded into the pipe
    self.preloaded = iterable_pre_load is not None

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

  @staticmethod
  def _create_wrapper(func, iter_index=0, is_valve=False):
    '''
    Creates a wrapped function that can be added to the class Pipe.
    The wrapper always puts the iterable in the correct location in the func's arguments.

    func - function to be wrapped
    iter_index - the index of the arguments to pass the iterable
    is_valve - should be true if the func is
    '''
    if is_valve:
      def wrapper(self, *args, **kargs):

        # arguments with the iterator in the proper location
        args_func = args[:iter_index] + (self.function_pipe,) + args[iter_index:]

        if self.valve:
          to_return = Pipe(
              iterable_pre_load = self.preloaded,
              function_pipe = func(*args_func, **kargs),
              reservoir = self.reservoir,
              valve = True,
            )

        elif self.preloaded:
          '''
          If the Pipe is preloaded with data and a valve is added the Pipe will run the
          pre loaded iterator and return the value.
          '''
          to_return = 

        else:

        return to_return

    else:
      def wrapper(self, *args, **kargs):
        args = args[:iter_index] + (self.function_pipe,) + args[iter_index:]
        return Pipe(
            iterable_pre_load = self.preloaded,
            function_pipe = func(*args, **kargs),
            reservoir = self.reservoir,
          )

    return wrapper

  @classmethod
  def add_method(cls, method, iter_index=0, method_name=None, no_over_write=True):
    '''
    method - method or function to be added
    iter_index - index of the iterator argument for method
      For enumerate(iterable, start=0) iter_index is 0
      For filter(function, iterable) iter_index is 1
    method_name - Unnecessary if method.__name__ is defined correctly.
      string that the method will be called by.
      Has precedence over method.__name__
    no_over_write - If True an AttributeError will be raised if 
    '''
    if not method_name:
      method_name = method.__name__

    if no_over_write and hasattr(cls, method_name):
      raise AttributeError('Point class already has the method ' + method.__name__)

    setattr(
        cls,
        method_name,
        cls._create_wrapper(method, iter_index)
      )

  @classmethod
  def add_map_method(cls, func, iter_index, method_name, no_over_write=True):
    cls.add_method(
        func = func,
        iter_index = iter_index,
        method_name = method_name,
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
  def test_call_iter_next(self):
    '''
    test iter, next, call.
    No extra methods added.
    '''
    data_1 = 1, 2, 3, 4
    data_2 = 5, 6, 7, 8

    pipe1 = Pipe()
    pipe1(data_1)
    self.assertEqual(tuple(pipe1), data_1)
    self.assertEqual(tuple(pipe1(data_2)), data_2)

    pipe1(data_1)
    for p, d in zip(pipe1, data_1):
      self.assertTrue(p is d)
    for p, d in zip(pipe1(data_2), data_2):
      self.assertTrue(p is d)

    pipe2 = Pipe()
    pipe2.valve = tuple
    self.assertEqual(pipe2(data_1), data_1)

    # preloaded iterable
    pipe3 = Pipe(data_1)
    self.assertEqual(tuple(pipe3), data_1)
    with self.assertRaises(StopIteration):
      next(pipe3)
    self.assertEqual(tuple(pipe3(data_2)), data_2)

  def test_add_method(self):

    # enumerate
    Pipe.add_method(enumerate)
    self.assertTrue(hasattr(Pipe, 'enumerate'))
    self.assertTrue(isinstance(Pipe.enumerate, types.FunctionType))
    self.assertTrue(isinstance(Pipe().enumerate, types.MethodType))
    with self.assertRaises(AttributeError):
      Pipe.add_method(enumerate)
    with self.assertRaises(AttributeError):
      Pipe.add_method(map, 'enumerate')

    # no_over_write is False
    Pipe.add_method(enumerate, no_over_write=False)
    self.assertTrue(hasattr(Pipe, 'enumerate'))
    self.assertTrue(isinstance(Pipe.enumerate, types.FunctionType))
    self.assertTrue(isinstance(Pipe().enumerate, types.MethodType))

    Pipe.add_method(enumerate, 'enumerate', no_over_write=False)
    self.assertTrue(hasattr(Pipe, 'enumerate'))
    self.assertTrue(isinstance(Pipe.enumerate, types.FunctionType))
    self.assertTrue(isinstance(Pipe().enumerate, types.MethodType))

    # test added method
    data_1 = 1, 2, 3, 4

    self.assertEqual(
        tuple(Pipe(data_1).enumerate()),
        tuple(enumerate(data_1))
      )
    self.assertEqual(
        tuple(Pipe(data_1).enumerate(2)),
        tuple(enumerate(data_1, 2))
      )
    self.assertEqual(
        tuple(Pipe(data_1).enumerate(start=2)),
        tuple(enumerate(data_1, start=2))
      )

    # clean up methods
    delattr(Pipe, 'enumerate')

  def test_add_map_method(self):
    Pipe.add_map_method(lambda a: a, pass)

  def test_pipe_creation_single_flow(self):
    '''
    Extending a Pipe with a
    '''
    data_1 = 1, 2, 3, 4


  def test_pipe_valve(self):
    data_1 = 1, 2, 3, 4
    data_1_min = min(data_1)

    # test method that directly passes the data through
    Pipe.add_method(
      partial(map, lambda val: val),
      method_name='pass_through')

    # min
    Pipe.add_method(min, is_valve=True)
    self.assertEqual(Pipe(data_1).min(), data_1_min)

    pipe_1 = Pipe().min()
    self.assertEqual(pipe_1(data_1), data_1_min)

    pipe2 = pipe_1

    # clean up
    delattr(Pipe, 'pass_through')








# class TestPipeCreateWrapper(unittest.TestCase):
#   def test_enumerate(self):
#     data_1 = 4, 5, 6
#     w1 = Pipe._create_wrapper(enumerate, 0)
#     self.assertEqual(
#         tuple(w1(data_1)),
#         tuple(enumerate(data_1))
#       )
#     self.assertEqual(
#         tuple(w1(data_1, 2)),
#         tuple(enumerate(data_1, 2))
#       )
#     self.assertEqual(
#         tuple(w1(data_1, start=3)),
#         tuple(enumerate(data_1, start=3))
#       )

#     # uses default for iter_index
#     w2 = Pipe._create_wrapper(enumerate)
#     self.assertEqual(
#         tuple(w2(data_1)),
#         tuple(enumerate(data_1))
#       )
#     self.assertEqual(
#         tuple(w2(data_1, 2)),
#         tuple(enumerate(data_1, 2))
#       )
#     self.assertEqual(
#         tuple(w2(data_1, start=3)),
#         tuple(enumerate(data_1, start=3))
#       )

#   def test_min(self):
#     data_1 = 4, 5, 6
#     w_1 = Pipe._create_wrapper(min, 0)
#     key_func = lambda val: 1 / val
#     self.assertEqual(
#         w_1(data_1),
#         min(data_1)
#       )
#     self.assertEqual(
#         w_1(data_1, key=key_func),
#         min(data_1, key=key_func)
#       )
#     self.assertEqual(
#         w_1(data_1, default=3),
#         min(data_1, default=3)
#       )
#     self.assertEqual(
#         w_1((), default=3),
#         min((), default=3)
#       )
#     self.assertEqual(
#         w_1(data_1, default=3, key=key_func),
#         min(data_1, default=3, key=key_func)
#       )

#   def test_filter(self):
#     data_1 = 4, 5, 6, 7
#     w1 = Pipe._create_wrapper(filter, 1)
#     filter_func = lambda val: val > 5
#     self.assertEqual(
#         tuple(w1(data_1, filter_func)),
#         tuple(filter(filter_func, data_1))
#       )


class TestFaucet(unittest.TestCase):
  def test_Faucet(self):
    data_1 = 1, 2, 3
    f1 = Valve(tuple, data_1)
    self.assertEqual(tuple(f1), data_1)
    for f, d in zip(f1, data_1):
      self.assertEqual(f, d)

  def test_iterable_object(self):
    '''
    tests functions that return an iterable object
    using sorted because it returns an iterable object
    '''
    test_function = sorted

    data_1 = 2, 1, 3
    data_1_sorted = test_function(data_1)
    data_2 = 5, 2, 6, 7, 2, 4, 6
    data_2_sorted = test_function(data_2)

    '''
    pass_whole is True
    should pass the whole sorted list back
    '''
    f1 = Valve(func=test_function, pre_pipe=data_1, pass_whole=True)
    f2 = Valve(func=test_function, pre_pipe=data_2, pass_whole=True)
    result_1 = next(f1)
    result_2 = next(f2)
    self.assertEqual(result_1, data_1_sorted)
    self.assertEqual(result_2, data_2_sorted)
    self.assertTrue(isinstance(result_1, list))
    self.assertTrue(isinstance(result_2, list))

    with self.assertRaises(StopIteration):
      next(f1)
    with self.assertRaises(StopIteration):
      next(f2)

    # test reuse with Reservoir
    s3 = Reservoir(data_1)
    f3 = Valve(func=test_function, pre_pipe=s3, pass_whole=True)
    self.assertTrue(next(f3), data_1_sorted)
    with self.assertRaises(StopIteration):
      next(f3)

    s3(data_2)
    self.assertTrue(next(f3), data_2_sorted)

    # pass_whole is False
    f4 = Valve(func=test_function, pre_pipe=data_1, pass_whole=False)
    self.assertTrue(next(f4) is data_1_sorted[0])
    for f, d in zip(f4, data_1_sorted[1:]):
      self.assertTrue(f is d)

    

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
    f1 = Valve(func=test_function, pre_pipe=data_1, pass_whole=True)
    result_1 = next(f1)
    self.assertTrue(result_1 is max_1)
    with self.assertRaises(StopIteration):
      next(f1)

    # pass_whole is False
    f2 = Valve(func=test_function, pre_pipe=data_1, pass_whole=False)
    result_1 = next(f2)
    self.assertTrue(result_1 is max_1)
    with self.assertRaises(StopIteration):
      next(f2)


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
