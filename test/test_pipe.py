import unittest, types
from itertools import zip_longest
from functools import partial

from functional_pipes import Pipe
from functional_pipes.pipe import Reservoir, Valve


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
        'min',
        'list',
        'expand',
        'add',
        'tuple',
      )

    for attr in to_del:
      if hasattr(Pipe, attr):
        delattr(Pipe, attr)

  def test_init_iter_call_next(self):
    '''
    test __inti__, __iter__, __call__, __next__.
    No extra methods added.
    '''
    data_1 = 1, 2, 3, 4
    data_2 = 5, 6, 7, 8
    data_3 = ()

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
    data = 1, 2, 3, 4

    self.assertEqual(
        tuple(Pipe(data).enumerate()),
        tuple(enumerate(data))
      )
    self.assertEqual(
        tuple(Pipe(data).enumerate(2)),
        tuple(enumerate(data, 2))
      )
    self.assertEqual(
        tuple(Pipe(data).enumerate(start=2)),
        tuple(enumerate(data, start=2))
      )

  def test_add_method_as_property(self):
    data = 1, 2, 3, 4

    Pipe.add_method(enumerate, as_property=True)

    self.assertEqual(
        tuple(Pipe(data).enumerate),
        tuple(enumerate(data))
      )

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
    data_3 = 5, 6, 3, 6, 2

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
        Pipe(data_2).min(),
        -5
      )

    # test function that shouldn't be starred
    self.assertEqual(
        Pipe(data_3).min(key=lambda a: 1 / a),
        max(data_3)
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
    data_2 = (1, 2), (3, 4)
    data_3 = dict(a=1, b=2), dict(a=3, b=4)

    Pipe.add_map_method(lambda a: a**2, 'square')

    self.assertEqual(
        tuple(Pipe(data_1).square()),
        tuple(d**2 for d in data_1)
      )

    # method call includes a value
    Pipe.add_map_method(min)
    self.assertEqual(
        tuple(Pipe(data_1).min(5, key=lambda a: 1 / a)),
        (5, 5, 7, 9)
      )

    self.assertEqual(
        tuple(Pipe(data_2).min()),
        (1, 3)
      )

    self.assertEqual(
        tuple(Pipe(data_2).min(key=lambda a: 1 / a)),
        (2, 4)
      )

    # single star
    Pipe.add_map_method(lambda a, b: a + b, 'add', star_wrap=True)

    self.assertEqual(
        tuple(Pipe(data_2).add()),
        (3, 7)
      )

    # double star
    Pipe.add_map_method(lambda a, b: a + b, 'add', double_star_wrap=True, no_over_write=False)

    self.assertEqual(
        tuple(Pipe(data_3).add()),
        (3, 7)
      )

  def test_pipe_valve_non_iterable(self):
    data_1 = 4, 2, 8, -5
    data_1_min = min(data_1)
    data_2 = ()

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

    # empty preloaded iterator
    with self.assertRaises(ValueError):
      print(Pipe(data_2).min())

  def test_pipe_valve_iterable(self):
    data_1 = [(1, 2), (3, 4), (5, 6)]

    Pipe.add_method(gener=list, is_valve=True)

    self.assertEqual(
        Pipe(data_1).list(),
        list(data_1)
      )

    pipe_1 = Pipe().list()

    self.assertEqual(
        pipe_1(data_1),
        list(data_1)
      )

  # def test_preloading_existing_pipe(self):
  #   '''
  #   https://github.com/BebeSparkelSparkel/functional_pipes/issues/9

  #   Give a created pipe data and then add aditional segments to it and a
  #   closing valve. After the valve is added it should execute and return
  #   the result.
  #   '''
  #   Pipe.add_method(gener=tuple, is_valve=True)

  #   data_1 = 1, 2, 3
  #   pipe_1 = Pipe()

  #   self.assertEqual(
  #       pipe_1(data_1).tuple(),
  #       data_1
  #     )





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
    valve_3 = Valve(func=test_function, iterator=resv_3, pass_args=(resv_3,))
    self.assertEqual(
        list(d for d, i in zip(valve_3, range(10))),
        sorted(data_1)
      )
    with self.assertRaises(StopIteration):
      next(valve_3)
    resv_3(data_2)
    self.assertTrue(next(valve_3), sorted(data_2))

    iter_4 = iter(data_1)
    valve_4 = Valve(func=test_function, iterator=iter_4, pass_args=(iter_4,))
    self.assertIs(next(valve_4), sorted(data_1)[0])
    for f, d in zip_longest(valve_4, sorted(data_1)[1:]):
      self.assertIs(f, d)

    # pass in a karg with pass_kargs
    iter_5 = iter(data_1)
    valve_5 = Valve(
        func = test_function,
        iterator = iter_5,
        pass_args = (iter_5,),
        pass_kargs = dict(reverse=True),
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

    iter_1 = iter(data_1)
    valve_1 = Valve(
        func = test_function,
        iterator = iter_1,
        pass_args = (iter_1,),
        empty_error = ValueError,
      )
    result_1 = next(valve_1)
    self.assertIs(result_1, max_1)
    with self.assertRaises(StopIteration):
      next(valve_1)

    # test with reservoir
    resr_2 = Reservoir(data_1)
    valve_2 = Valve(
        func=test_function,
        iterator=resr_2,
        pass_args=(resr_2,),
        empty_error=ValueError
      )
    self.assertIs(next(valve_2), max_1)
    with self.assertRaises(StopIteration):
      next(valve_2)
    resr_2(data_2)
    self.assertIs(next(valve_2), max_2)

  def test_empty_iter(self):
    '''
    The iterator that the valve has should be completely consumed when the
    function valve applies to it is complete.
    '''
    data_1 = 2, 1, 3

    iter_1 = iter(data_1)
    valve_1 = Valve(
        func = next,
        iterator = iter_1,
        pass_args = (iter_1,),
        empty_error = StopIteration,
      )
    next(valve_1)
    with self.assertRaises(StopIteration):
      next(valve_1)

  def test_whole_return(self):
    data_1 = 1, 2, 3, 4
    iter_1 = iter(data_1)

    valve_1 = Valve(list, iter_1, (iter_1,))

    self.assertEqual(valve_1.whole_return(), list(data_1))


class TestReservoir(unittest.TestCase):
  def test_init(self):
    Reservoir()

    data_1 = 1, 2, 3, 4
    sp1 = Reservoir(data_1)
    self.assertEqual(tuple(sp1.iterator), data_1)

    sp2 = Reservoir(data_1)
    self.assertIsNot(sp1, sp2)

  def test_iter_next_call(self):
    # test iter and next
    sp1 = Reservoir()

    with self.assertRaises(StopIteration):
      next(sp1)

    data_1 = tuple(range(10))
    sp1(range(10))

    for s, d in zip_longest(sp1, data_1):
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

  def test_drain_then_fill(self):
    data_1 = 1, 2, 4, 8
    data_2 = 5, 3, 6, 9

    res_1 = Reservoir(data_1)
    tuple(res_1)
    res_1(data_2)

    '''
    Should not trigger StopIteration in Reservoir.iterator. Iterator
    is now empty and should be allowed to be filled.
    '''
    for i in range(len(data_2)):
      next(res_1)
    res_1(data_1)

  def test_not_empty(self):
    data_1 = 1, 2
    data_2 = ()

    res_1 = Reservoir(data_1)
    self.assertTrue(res_1.not_empty())

    # tuple(zip(data_1, res_1))
    tuple(res_1)
    self.assertFalse(res_1.not_empty())

    res_1(data_1)
    self.assertTrue(res_1.not_empty())

    res_2 = Reservoir()
    self.assertFalse(res_2.not_empty())

    res_2(data_1)
    self.assertTrue(res_2.not_empty())




class Expand:
  def __init__(self, iterable):
    self.iterable = iter(iterable)
    self.nexts = None

  def __next__(self):
    try:
      return next(self.nexts)

    except TypeError:
      next(self.iterable)

      self.nexts = iter(range(2))
      return next(self)

    except StopIteration as err:
      self.nexts = None
      return next(self)

  def __iter__(self):
    return self

class TestExpand(unittest.TestCase):
  def test_Expand(self):
    data_1 = 1, 2, 3
    result_1 = (0, 1) * len(data_1)

    self.assertEqual(
        tuple(Expand(data_1)),
        result_1
      )



if __name__ == '__main__':
  unittest.main()
