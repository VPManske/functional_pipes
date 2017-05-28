import unittest
import types

from functional_pipes import Pipe, Reservoir, Valve


class TestPipe(unittest.TestCase):
  def tearDown(self):
    to_del = (
        'enumerate',
        'filter',
        'func_after_iter',
        'extra_input_last',
        'extra_input_first',
        'extra_input_middle',
        'min_key_arg',
        'min',
        'square',
        'pass_through',
        'min'
      )

    for attr in to_del:
      if hasattr(Pipe, attr):
        delattr(Pipe, attr)

  def test_call_iter_next(self):
    '''
    test iter, next, call.
    No extra methods added.
    '''
    data_1 = 1, 2, 3, 4
    data_2 = 5, 6, 7, 8

    pipe_1 = Pipe()
    pipe_1(data_1)
    self.assertEqual(tuple(pipe_1), data_1)
    self.assertEqual(tuple(pipe_1(data_2)), data_2)

    pipe_1(data_1)
    for p, d in zip(pipe_1, data_1):
      self.assertTrue(p is d)
    for p, d in zip(pipe_1(data_2), data_2):
      self.assertTrue(p is d)

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
      Pipe.add_method(map, gener_name='enumerate')

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

    # stared arg
    Pipe.add_method


  def test_add_method_star_int(self):
    '''
    Tests if the star wrapper is properly applied to a function if the
    star_wrap argument to add_method is an integer that specifies the
    argument index in args.
    '''
    data_1 = (1, 2), (3, 4), (5, 6)
    def filter_1_1(a):
      return 2 * a[0] > a[1]
    def filter_1_2(a, b):
      return 2 * a > b
    data_1_filtered = tuple(filter(filter_1_1, data_1))
    self.assertEqual(
        data_1_filtered,
        tuple(filter(lambda pt: filter_1_2(*pt), data_1))
      )

    # function before iterator. filter(function, iterator)
    Pipe.add_method(
        gener = filter,
        iter_index = 1,
        star_wrap = 0,
      )
    self.assertTrue(hasattr(Pipe, 'filter'))
    self.assertEqual(
        tuple(Pipe(data_1).filter(filter_1_1)),
        data_1_filtered
      )
    self.assertEqual(
        tuple(Pipe(data_1).filter(filter_1_2)),
        data_1_filtered
      )

    # function after iterator
    def func_after_iter(iterator, function):
      for val in iterator:
        if function(val):
          yield val

    Pipe.add_method(
        gener = func_after_iter,
        star_wrap = 1,
      )
    self.assertEqual(
        tuple(Pipe(data_1).func_after_iter(filter_1_1)),
        data_1_filtered
      )
    self.assertEqual(
        tuple(Pipe(data_1).func_after_iter(filter_1_2)),
        data_1_filtered
      )

    # function with extra argument at the end
    extra_val = 777
    def extra_input_last(iterator, function, extra):
      if extra != extra_val:
        raise ValueError('extra != extra_val, {} != {}'.format(extra, extra_val))
      for val in iterator:
        if function(val):
          yield val

    Pipe.add_method(
        gener = extra_input_last,
        star_wrap = 1,
      )
    self.assertEqual(
        tuple(Pipe(data_1).extra_input_last(filter_1_1, extra_val)),
        data_1_filtered
      )
    self.assertEqual(
        tuple(Pipe(data_1).extra_input_last(filter_1_2, extra_val)),
        data_1_filtered
      )

    # function with extra argument at the beginning
    extra_val = 888
    def extra_input_first(extra, iterator, function):
      if extra != extra_val:
        raise ValueError('extra != extra_val, {} != {}'.format(extra, extra_val))
      for val in iterator:
        if function(val):
          yield val

    Pipe.add_method(
        gener = extra_input_first,
        iter_index = 1,
        star_wrap = 2,
      )
    self.assertEqual(
        tuple(Pipe(data_1).extra_input_first(extra_val, filter_1_1)),
        data_1_filtered
      )
    self.assertEqual(
        tuple(Pipe(data_1).extra_input_first(extra_val, filter_1_2)),
        data_1_filtered
      )

    # function with extra argument in the middle
    extra_val = 999
    def extra_input_middle(iterator, extra, function):
      if extra != extra_val:
        raise ValueError('extra != extra_val, {} != {}'.format(extra, extra_val))
      for val in iterator:
        if function(val):
          yield val

    Pipe.add_method(
        gener = extra_input_middle,
        star_wrap = 2,
      )
    self.assertEqual(
        tuple(Pipe(data_1).extra_input_middle(extra_val, filter_1_1)),
        data_1_filtered
      )
    self.assertEqual(
        tuple(Pipe(data_1).extra_input_middle(extra_val, filter_1_2)),
        data_1_filtered
      )

    # test with a valve function with a star arg
    def min_key_arg(iterable, key):
      return min(iterable, key=key)
    Pipe.add_method(
        gener = min_key_arg,
        is_valve = True,
        star_wrap = 1,
      )
    self.assertTrue(hasattr(Pipe, 'min_key_arg'))
    self.assertEqual(
        Pipe(data_1).min_key_arg(lambda a, b: 1 / a),
        (5, 6)
      )

  def test_add_method_star_str(self):
    '''
    Tests if the star wrapper is properly applied to a function if the
    star_wrap argument to add_method is an string that specifies the
    argument key in kargs.
    '''
    data_1 = (1, 2), (3, 4), (5, 6)
    data_2 = 4, 2, 8, -5

    Pipe.add_method(
        gener = min,
        is_valve = True,
        star_wrap = 'key',
      )
    self.assertEqual(
        Pipe(data_1).min(key=lambda a, b: 1 / a),
        (5, 6)
      )
    self.assertEqual(
        Pipe(data_2 ).min(),
        -5
      )

  def test_add_method_double_star_int(self):
    data_1 = tuple(dict(a=a, b=b) for a, b in ((1, 2), (3, 4), (5, 6)))

    def min_key_arg(iterable, key):
      return min(iterable, key=key)
    Pipe.add_method(
        gener = min_key_arg,
        is_valve = True,
        double_star_wrap = 1,
      )
    self.assertTrue(hasattr(Pipe, 'min_key_arg'))
    self.assertEqual(
        Pipe(data_1).min_key_arg(lambda a, b: 1 / a),
        dict(a=5, b=6)
      )

  def test_add_method_double_star_str(self):
    data_1 = tuple(dict(a=a, b=b) for a, b in ((1, 2), (3, 4), (5, 6)))

    def min_key_arg(iterable, key):
      return min(iterable, key=key)
    Pipe.add_method(
        gener = min_key_arg,
        is_valve = True,
        double_star_wrap = 'key',
      )
    self.assertTrue(hasattr(Pipe, 'min_key_arg'))
    self.assertEqual(
        Pipe(data_1).min_key_arg(key=lambda a, b: 1 / a),
        dict(a=5, b=6)
      )

  def test_add_map_method(self):
    data_1 = 1, 2, 7, 9
    data_1_squared = tuple(d**2 for d in data_1)

    Pipe.add_map_method(lambda a: a**2, 'square')

    self.assertEqual(tuple(Pipe(data_1).square()), data_1_squared)

  def test_pipe_valve(self):
    data_1 = 4, 2, 8, -5
    data_1_min = min(data_1)

    # test method that directly passes the data through
    Pipe.add_map_method(lambda val: val, 'pass_through')
    # min
    Pipe.add_method(min, is_valve=True, empty_error=ValueError)

    '''
    The Pipe has been preloaded and a valve has been added to the pipe.
    When the preloaded and a valve is added the reservoir should be drained
    by the pipe into the valve function and the result should be returned.
    '''
    self.assertEqual(
        Pipe(data_1).min(),
        data_1_min
      )
    self.assertEqual(
        Pipe(data_1).pass_through().min(),
        data_1_min
      )

    '''
    Pipe has not been preloaded and a Pipe should be returned.
    '''
    pipe_1 = Pipe().min()
    self.assertEqual(pipe_1(data_1), data_1_min)
    self.assertEqual(pipe_1(data_1), data_1_min)  # not a repeat

    pipe_2 = Pipe().pass_through().min()
    self.assertEqual(pipe_2(data_1), data_1_min)
    self.assertEqual(pipe_2(data_1), data_1_min)  # not a repeat

    pip_3 = Pipe().min().pass_through()
    self.assertEqual(next(pip_3(data_1)), data_1_min)

    pip_4 = Pipe().min().min()
    self.assertEqual(pipe_1(data_1), data_1_min)

    pipe_5 = pipe_1.pass_through()
    self.assertEqual(
        next(pipe_5(data_1)),
        next(pip_3(data_1))
      )

    pipe_6 = pipe_1.min()
    self.assertEqual(
        pipe_6(data_1),
        pip_4(data_1)
      )


class TestValve(unittest.TestCase):
  def test_iterable_object(self):
    '''
    tests functions that return an iterable object
    using sorted because it returns an iterable object
    '''
    test_function = sorted

    data_1 = 2, 1, 3
    data_2 = 5, 2, 6, 7, 2, 4, 6

    # test reuse with Reservoir
    resv_3 = Reservoir(data_1)
    valve_3 = Valve(func=test_function, pass_args=(resv_3,))
    self.assertTrue(list(valve_3), sorted(data_1))
    with self.assertRaises(StopIteration):
      next(valve_3)
    resv_3(data_2)
    self.assertTrue(next(valve_3), sorted(data_2))

    valve_4 = Valve(func=test_function, pass_args=(data_1,))
    self.assertTrue(next(valve_4) is sorted(data_1)[0])
    for f, d in zip(valve_4, sorted(data_1)[1:]):
      self.assertTrue(f is d)

    # pass in a karg with pass_kargs
    valve_5 = Valve(
        func=test_function,
        pass_args=(iter(data_1),),
        pass_kargs=dict(reverse=True),
      )
    self.assertEqual(list(valve_5), sorted(data_1, reverse=True))
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

    valve_1 = Valve(
        func = test_function,
        pass_args = (iter(data_1),),
        empty_error = ValueError,
      )
    result_1 = next(valve_1)
    self.assertTrue(result_1 is max_1)
    with self.assertRaises(StopIteration):
      next(valve_1)

    # test with reservoir
    resr_2 = Reservoir(data_1)
    valve_2 = Valve(func=test_function, pass_args=(resr_2,), empty_error=ValueError)
    self.assertTrue(next(valve_2) is max_1)
    with self.assertRaises(StopIteration):
      next(valve_2)
    resr_2(data_2)
    self.assertTrue(next(valve_2) is max_2)





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
