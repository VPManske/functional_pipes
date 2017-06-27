import unittest

from functional_pipes import Pipe


class TestMethods(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    Pipe.load('operator_pipes')

  @classmethod
  def tearDownClass(self):
    Pipe.unload('operator_pipes')

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