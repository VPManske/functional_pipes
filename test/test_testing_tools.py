import unittest, io

from functional_pipes import Pipe
from functional_pipes.testing_tools import add_class_methods, method_names


class TestMethods(unittest.TestCase):
  @classmethod
  def setUpClass(self):
    add_class_methods(Pipe)

  @classmethod
  def tearDownClass(self):
    for name in method_names:
      delattr(Pipe, name)

  def test_limit_size(self):
    data_1 = 1, 2, 3

    self.assertEqual(
        tuple(Pipe(data_1).limit_size(3)),
        data_1
      )

    with self.assertRaises(ValueError):
      tuple(Pipe(data_1).limit_size(2))



class TestMapMethods(unittest.TestCase):
  @classmethod
  def setUpClass(self):
    add_class_methods(Pipe)

  @classmethod
  def tearDownClass(self):
    for name in method_names:
      delattr(Pipe, name)

  def test_look_in(self):
    data_1 = [1, 2, 3, 4]
    in_1 = []
    tuple(Pipe(data_1).look_in(in_1))
    self.assertEqual(in_1, data_1)


if __name__ == '__main__':
  unittest.main()