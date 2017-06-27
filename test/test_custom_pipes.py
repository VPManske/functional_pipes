import unittest, io
from itertools import chain

from functional_pipes import Pipe


class TestMethods(unittest.TestCase):
  @classmethod
  def setUpClass(self):
    Pipe.load('built_in_functions', 'custom_pipes', 'testing_tools')

  @classmethod
  def tearDownClass(self):
    Pipe.unload('built_in_functions', 'custom_pipes', 'testing_tools')

  def test_zip_internal(self):
    data_1 = (1, 2, 3), (4, 5, 6), (7, 8, 9)
    data_1_zipped = tuple(zip(*data_1))
    data_2 = ()

    self.assertEqual(
        tuple(Pipe(data_1).zip_internal()),
        data_1_zipped
      )

    pipe_1 = Pipe().zip_internal()
    self.assertEqual(
        tuple(pipe_1(data_1)),
        data_1_zipped
      )
    self.assertEqual(tuple(pipe_1(data_1)), data_1_zipped) # reload the pipe

    self.assertEqual(
        tuple(Pipe(data_2).zip_internal()),
        ()
      )

  def test_zip_to_dict(self):
    data_1 = ('a', (1, 2)), ('b', (3, 4))
    result_1 = {'a': 1, 'b': 3}, {'a': 2, 'b': 4}

    self.assertEqual(
        tuple(Pipe(data_1).zip_to_dict()),
        result_1
      )

    self.assertEqual(
        Pipe(data_1).zip_to_dict().tuple(),
        result_1
      )

    pipe_1 = Pipe().zip_to_dict().limit_size(2).tuple()
    self.assertEqual(pipe_1(data_1), result_1)



if __name__ == '__main__':
  unittest.main()

