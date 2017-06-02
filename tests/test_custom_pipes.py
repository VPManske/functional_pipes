import unittest, io

from functional_pipes import Pipe, custom_pipes


Pipe.add_map_method(lambda val: val, 'same')


class TestMethods(unittest.TestCase):
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

  def test_dict_zip(self):
    data_1 = dict(a=(1, 2), b=(3, 4)),
    data_1_dz = dict(a=1, b=3), dict(a=2, b=4)

    self.assertEqual(
        tuple(Pipe(data_1).dict_zip()),
        data_1_dz
      )

    self.assertEqual(
        tuple(Pipe(2 * data_1).dict_zip()),
        2 * data_1_dz
      )

    pipe_1 = Pipe().dict_zip()
    self.assertEqual(
        tuple(pipe_1(2 * data_1)),
        2 * data_1_dz
      )
    self.assertEqual(tuple(pipe_1(data_1)), data_1_dz) # reload the pipe


if __name__ == '__main__':
  unittest.main()