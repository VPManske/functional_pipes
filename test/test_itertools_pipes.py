import unittest, io
from itertools import chain

from functional_pipes import Pipe
from functional_pipes.itertools_pipes import add_class_methods, method_names


class TestMethods(unittest.TestCase):
  @classmethod
  def setUpClass(self):
    add_class_methods(Pipe)

  @classmethod
  def tearDownClass(self):
    for name in method_names:
      delattr(Pipe, name)

  # def test_groupby(self):
  #   data_1 = ('a', 1), ('b', 2), ('a', 3), ('b', 4)
  #   data_2 = ('a', 1), ('a', 3), ('b', 2), ('b', 4)
  #   self.assertEqual(
  #       Pipe(data_1).groupby(lambda key: key[0]),

  #     )



if __name__ == '__main__':
  unittest.main()

