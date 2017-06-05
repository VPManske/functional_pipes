import unittest, types

from functional_pipes.pipe import Pipe, Reservoir
from functional_pipes.bypass import Drip, Bypass


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