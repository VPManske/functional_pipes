import unittest, io

from functional_pipes import Pipe
from functional_pipes.operator_pipes import add_class_methods, method_names


class TestMethods(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    add_class_methods(Pipe)

  @classmethod
  def tearDownClass(self):
    for name in method_names:
      delattr(Pipe, name)

  def test_mul(self):
    data_1 = 1, 2, 3, 4

    self.assertEqual(
        tuple(Pipe(data_1).mul(5)),
        tuple(5 * val for val in data_1)
      )

    pipe_1 = Pipe().mul(5)
    self.assertEqual(
        tuple(pipe_1(data_1)),
        tuple(5 * val for val in data_1)
      )

  def test_add(self):
    data_1 = 1, 2, 3, 4

    self.assertEqual(
        tuple(Pipe(data_1).add(5)),
        tuple(5 + val for val in data_1)
      )

    pipe_1 = Pipe().add(5)
    self.assertEqual(
        tuple(pipe_1(data_1)),
        tuple(5 + val for val in data_1)
      )

if __name__ == '__main__':
  unittest.main()