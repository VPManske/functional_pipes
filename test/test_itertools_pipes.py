import unittest, io
import itertools as it

from functional_pipes import Pipe


class TestMethods(unittest.TestCase):
  @classmethod
  def setUpClass(self):
    Pipe.load('itertools_pipes')

  @classmethod
  def tearDownClass(self):
    Pipe.unload('itertools_pipes')

  def test_groupby_no_key(self):
    data = 1, 2, 3, 1, 2, 3, 4

    to_tuple = lambda groups: tuple((key, tuple(group)) for key, group in groups)

    self.assertEqual(
        to_tuple(Pipe(data).groupby()),
        to_tuple(it.groupby(data))
      )



if __name__ == '__main__':
  unittest.main()

