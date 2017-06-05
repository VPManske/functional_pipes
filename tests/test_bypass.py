import unittest, types

from functional_pipes.pipe import Pipe, Reservoir
from functional_pipes.bypass import Drip, Bypass


class TestPipeBypasses(unittest.TestCase):
  @classmethod
  def setUpClass(self):
    Pipe.add_method(gener=map, iter_index=1)
    Pipe.add_method(gener=filter, iter_index=1)
    Pipe.add_method(Expand)

  @classmethod
  def tearDownClass(self):
    delattr(Pipe, 'filter')
    delattr(Pipe, 'map')
    delattr(Pipe, 'Expand')

  def test_carry_key_no_size_change(self):
    data_1 = (1, 2), (3, 4), (5, 6)
    result_1 = (1, 4), (3, 8), (5, 12)

    self.assertEqual(
        tuple(Pipe(data_1).carry_key.map(lambda b: 2 * b).re_key),
        result_1
      )

    pipe_1 = Pipe(
      ).carry_key.map(lambda b: 2 * b
      ).re_key
    self.assertEqual(tuple(pipe_1(data_1)), result_1)
    self.assertEqual(tuple(pipe_1(data_1)), result_1)  # not a repeat

  def test_carry_key_shrink(self):
    data_1 = (1, 2), (3, 4), (5, 6)
    filter_1 = lambda val: val != 4
    result_1 = (1, 2), (5, 6)

    self.assertEqual(
        tuple(Pipe(data_1).carry_key.filter(filter_1).re_key),
        result_1
      )

  def test_carry_key_expand(self):
    data_1 = (1, 2), (3, 4), (5, 6)
    result_1 = (1, 0), (1, 1), (3, 0), (3, 1), (5, 0), (5, 1)

    self.assertEqual(
        tuple(Pipe(data_1).carry_key.Expand().re_key),
        result_1
      )

  def test_carry_value(self):
    # no_size_change
    data_1 = (1, 2), (3, 4), (5, 6)
    result_1 = (2, 2), (6, 4), (10, 6)
    self.assertTrue(hasattr(Pipe, 'carry_key'))
    self.assertTrue(hasattr(Pipe, 'carry_value'))
    self.assertEqual(
        tuple(Pipe(data_1).carry_value.map(lambda a: 2 * a).re_value),
        result_1
      )

    # shrink
    data_2 = (1, 2), (3, 4), (5, 6)
    filter_2 = lambda val: val != 3
    result_2 = (1, 2), (5, 6)
    self.assertEqual(
        tuple(Pipe(data_2).carry_value.filter(filter_2).re_value),
        result_2
      )

    # expand
    data_3 = (1, 2), (3, 4)
    result_3 = (0, 2), (1, 2), (0, 4), (1, 4)

    self.assertEqual(
        tuple(Pipe(data_3).carry_value.Expand().re_value),
        result_3
      )



class TestBypass(unittest.TestCase):
  def tearDown(self):
    '''
    Remove the added methods from pipe.Pipe
    '''
    to_del = (
        'square',
      )

    for attr in to_del:
      if hasattr(Pipe, attr):
        delattr(Pipe, attr)

  def test_init_next_iter(self):
    Pipe.add_map_method(lambda a: a**2, 'square')

    data_1 = (1, 2), (3, 4), (5, 6)
    drip_1 = Drip()
    res_1 = Reservoir(data_1)
    pipe_1 = Pipe(reservoir = drip_1).square()
    result_1 = tuple((a, b**2) for a, b in data_1)

    def carry_key(key_val):
      return key_val[0], key_val[1]

    def re_key(key, bypass_val):
      return key, bypass_val

    bpp = Bypass(
        bypass = pipe_1,
        iterable = res_1,
        drip_handle = drip_1,
        split = carry_key,
        merge = re_key,
      )

    self.assertEqual(tuple(bpp), result_1)

  def test_shrinking_bypass(self):
    '''
    Where the bypass returns less items than put in it.
    Like if it contains a filter.
    '''
    data_1 = (1, 2), (3, 4), (5, 6)
    drip_1 = Drip()
    filter_func = filter(lambda b: b != 4, drip_1)
    data_1_filtered = (1, 2), (5, 6)

    def carry_key(key_val):
      return key_val[0], key_val[1]

    def re_key(key, bypass_val):
      return key, bypass_val


    bpp = Bypass(
        bypass = filter_func,
        iterable = data_1,
        drip_handle = drip_1,
        split = carry_key,
        merge = re_key,
      )

    self.assertEqual(
        tuple(bpp),
        data_1_filtered
      )

  def test_expanding_bypass(self):
    '''
    Where the bypass returns less items than put in it.
    Like if it contains a filter.
    '''
    data_1 = (1, 2), (3, 4), (5, 6)
    drip_1 = Drip()
    result_1 = (1, 0), (1, 1), (3, 0), (3, 1), (5, 0), (5, 1)

    def carry_key(key_val):
      return key_val[0], key_val[1]

    def re_key(key, bypass_val):
      return key, bypass_val

    bpp_1 = Bypass(
        bypass = Expand(drip_1),
        iterable = data_1,
        drip_handle = drip_1,
        split = carry_key,
        merge = re_key,
      )

    self.assertEqual(tuple(bpp_1), result_1)

    # empty data
    data_2 = ()
    drip_2 = Drip()
    bpp_2 = Bypass(
        bypass = Expand(drip_2),
        iterable = data_2,
        drip_handle = drip_2,
        split = carry_key,
        merge = re_key,
      )

    self.assertEqual(tuple(bpp_2), ())


class TestDrip(unittest.TestCase):
  def test_init_call_next_iter(self):
    drip_1 = Drip()
    with self.assertRaises(Drip):
      print('Drip not raised:', next(drip_1))
    drip_1(1)
    self.assertEqual(next(drip_1), 1)
    drip_1(None)
    self.assertIsNone(next(drip_1))
    with self.assertRaises(Drip):
      print('Drip not raised:', next(drip_1))


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