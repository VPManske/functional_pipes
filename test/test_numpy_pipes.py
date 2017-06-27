import unittest
import numpy as np

from functional_pipes import Pipe


class TestMethods(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    Pipe.load('numpy_pipes')

  @classmethod
  def tearDownClass(self):
    Pipe.unload('numpy_pipes')

  def test_fromiter(self):
    data_1 = 1, 2, 3

    self.assertTrue(np.array_equal(
        Pipe(data_1).fromiter(float),
        np.array(data_1)
      ))

    pipe_1 = Pipe().fromiter(float)
    self.assertTrue(np.array_equal(
        pipe_1(data_1),
        np.array(data_1)
      ))


if __name__ == '__main__':
  unittest.main()