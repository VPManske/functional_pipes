import unittest, io
import itertools as it

from functional_pipes import Pipe


class TestMethods(unittest.TestCase):
  @classmethod
  def setUpClass(self):
    Pipe.load('built_in_functions', 'itertools_pipes')

  @classmethod
  def tearDownClass(self):
    Pipe.unload('built_in_functions', 'itertools_pipes')

  def test_groupby_no_key(self):
    data = 1, 2, 3, 1, 2, 3, 4

    to_tuple = lambda groups: tuple((key, tuple(group)) for key, group in groups)

    self.assertEqual(
        to_tuple(Pipe(data).groupby()),
        to_tuple(it.groupby(data))
      )

  def test_groupby_with_key(self):
    data = 1, 2, 3, 1, 2, 3, 4

    key = lambda val: val % 2

    to_tuple = lambda groups: tuple((key, tuple(group)) for key, group in groups)

    ref = to_tuple(it.groupby(data, key))

    self.assertEqual(
        to_tuple(Pipe(data).groupby(key)),
        ref
      )

    pipe_reuse = Pipe().groupby(key)

    self.assertEqual(
        to_tuple(pipe_reuse(data)),
        ref
      )
    self.assertEqual(
        to_tuple(pipe_reuse(data)),
        ref
      )  # reload pipe

  def test_groupby_key(self):
    data = (1, 2), (3, 4), (1, 5)

    key = lambda key_val: key_val[0]

    to_tuple = lambda groups: tuple((key, tuple(group)) for key, group in groups)

    ref = to_tuple(it.groupby(data, key))

    self.assertEqual(
        to_tuple(Pipe(data).groupby_key()),
        ref
      )

    pipe_reuse = Pipe().groupby_key()

    self.assertEqual(
        to_tuple(pipe_reuse(data)),
        ref
      )
    self.assertEqual(
        to_tuple(pipe_reuse(data)),
        ref
      )  # reload pipe


if __name__ == '__main__':
  unittest.main()

