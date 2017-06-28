import unittest

from functional_pipes import Pipe
from test_bypass import Expand


class TestPipeBypasses(unittest.TestCase):
  @classmethod
  def setUpClass(self):
    Pipe.add_method(gener=filter, iter_index=1)
    Pipe.add_method(Expand)
    Pipe.add_method(gener=tuple, is_valve=True)

  @classmethod
  def tearDownClass(self):
    delattr(Pipe, 'filter')
    delattr(Pipe, 'Expand')
    delattr(Pipe, 'tuple')

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

  def test_wrong_closing_bypass(self):
    '''
    A bypass that is closed with the wrong closer should raise an TypeError.
    '''
    Pipe().carry_key.re_key

    with self.assertRaises(TypeError):
      Pipe().carry_key.re_value

  def test_pass_key(self):
    data = dict(a=1, b=2, c=3), dict(a=4, b=5, c=6), dict(a=7, b=8, c=9)

    self.assertEqual(
        Pipe(data
          ).carry_dict['b'].map(lambda val: 2 * val
          ).return_dict.tuple(),
        (dict(a=1, b=4, c=3), dict(a=4, b=10, c=6), dict(a=7, b=16, c=9))
      )

  def test_keyed(self):
    data = 1, 2, 3, 4
    ref = tuple((val, 2 * val) for val in data)

    self.assertEqual(
        Pipe(data).keyed.map(lambda val: 2 * val).tuple(),
        ref
      )

    pipe_def = Pipe().keyed.map(lambda val: 2 * val).tuple()
    self.assertEqual(pipe_def(data), ref)
    self.assertEqual(pipe_def(data), ref)  # not a reference

  def test_dict_key(self):
    data = dict(a=1, b=2, c=3), dict(a=4, b=5, c=6), dict(a=7, b=8, c=9)

    self.assertEqual(
        Pipe(data
          ).dict_key['b'].map(lambda val: 2 * val
          ).tuple(),
        (dict(a=1, b=4, c=3), dict(a=4, b=10, c=6), dict(a=7, b=16, c=9))
      )
