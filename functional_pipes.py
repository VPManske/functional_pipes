import types


class Spigot:
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
      raise StopIteration('Spigot is empty.')


class Faucet:
  '''
  Transforms functions that accept iterators and returns a value into a generator.
  This allow functions that are not generators to be passed into a pipe.

  IMPROVEMENT:
  __next__ has a lot of dynamic checks if this could be doen in __init__ it would
    help the pipeline performance.

  Example with sorted:
    >>> data_1 = 2, 1, 3
    >>> f1 = Faucet(func=sorted, pre_pipe=data_1, pass_whole=True)
    >>> next(f1)
    [1, 2, 3]
    >>> next(f1)
    raises StopIteration

    >>> f2 = Faucet(func=sorted, pre_pipe=data_1, pass_whole=False)
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
    >>> f1 = Faucet(func=test_function, pre_pipe=data_1, pass_whole=True)
    >>> result_1 = next(f1)
    3
    >>> result_1 = next(f1)
    raises StopIteration
  '''

  def __init__(self, func, pre_pipe, pass_whole=False):
    '''
    func - A function that should consume the whole iterable and return an object.
      If the returned object is iterable, Faucet will pass one value of the object iterator
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
  def __init__(self, function_pipe=None, spigot=None):
    self.spigot = spigot if spigot else Spigot()
    self.function_pipe = function_pipe if function_pipe else self.spigot
    self.faucet = None

  def __call__(self, iterable):
    self.spigot(iterable)
    if self.faucet:
      return self.faucet(self)

    return self

  def __iter__(self):
    return self

  def __next__(self):
    return next(self.function_pipe)

  @classmethod
  def add_method(cls, function, properties):


  def map(self, func):
    return Pipe(
        function_pipe = map(func, self.function_pipe),
        spigot = self.spigot,
      )


# enumerate(iterable, start=0)
# min(iterable, *[, key, default])
# filter(function, iterable)






import unittest


class TestPipe(unittest.TestCase):
  def test_call_iter_next(self):
    '''
    test iter, next, call.
    Call without faucet.
    No extra methods added.
    '''
    pipe1 = Pipe()
    data_1 = 1, 2, 3, 4
    data_2 = 5, 6, 7, 8
    pipe1(data_1)
    self.assertEqual(tuple(pipe1), data_1)
    self.assertEqual(tuple(pipe1(data_2)), data_2)

    pipe1(data_1)
    for p, d in zip(pipe1, data_1):
      self.assertTrue(p is d)
    for p, d in zip(pipe1(data_2), data_2):
      self.assertTrue(p is d)


    pipe2 = Pipe()
    pipe2.faucet = tuple
    self.assertEqual(pipe2(data_1), data_1)


  def test_map(self):
    pipe1 = Pipe().map(lambda val: 2 * val)
    data_1 = 1, 2, 3, 4
    data_2 = 5, 6, 7, 8
    self


class TestFaucet(unittest.TestCase):
  def test_Faucet(self):
    data_1 = 1, 2, 3
    f1 = Faucet(tuple, data_1)
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
    f1 = Faucet(func=test_function, pre_pipe=data_1, pass_whole=True)
    f2 = Faucet(func=test_function, pre_pipe=data_2, pass_whole=True)
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

    # test reuse with Spigot
    s3 = Spigot(data_1)
    f3 = Faucet(func=test_function, pre_pipe=s3, pass_whole=True)
    self.assertTrue(next(f3), data_1_sorted)
    with self.assertRaises(StopIteration):
      next(f3)

    s3(data_2)
    self.assertTrue(next(f3), data_2_sorted)

    # pass_whole is False
    f4 = Faucet(func=test_function, pre_pipe=data_1, pass_whole=False)
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
    f1 = Faucet(func=test_function, pre_pipe=data_1, pass_whole=True)
    result_1 = next(f1)
    self.assertTrue(result_1 is max_1)
    with self.assertRaises(StopIteration):
      next(f1)

    # pass_whole is False
    f2 = Faucet(func=test_function, pre_pipe=data_1, pass_whole=False)
    result_1 = next(f2)
    self.assertTrue(result_1 is max_1)
    with self.assertRaises(StopIteration):
      next(f2)


class TestSpigot(unittest.TestCase):
  def test_init(self):
    Spigot()

    data_1 = 1, 2, 3, 4
    sp1 = Spigot(data_1)
    self.assertEqual(tuple(sp1.iterator), data_1)

    sp2 = Spigot(data_1)
    self.assertTrue(sp1 is not sp2)

  def test_iter_next_call(self):
    # test iter and next
    sp1 = Spigot()

    with self.assertRaises(StopIteration):
      next(sp1)

    data_1 = tuple(range(10))
    sp1(range(10))

    for s, d in zip(sp1, data_1):
      self.assertEqual(s, d)


    # test call
    sp2 = Spigot()

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

    # call when spigot not yet empty
    sp2(data_1)
    with self.assertRaises(ValueError):
      sp2(data_1)


if __name__ == '__main__':
  unittest.main()