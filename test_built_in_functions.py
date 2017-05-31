import unittest

from pipe import Pipe
import built_in_functions


Pipe.add_map_method(lambda val: val, 'same')


class TestBuiltInFunctions(unittest.TestCase):
  def test_all(self):
    data_1 = 1, 1, 1
    data_2 = 1, 0, 0
    data_3 = ()

    self.assertTrue(Pipe(data_1).all())
    self.assertFalse(Pipe(data_2).all())
    self.assertTrue(Pipe(data_3).all())

    pipe_1 = Pipe().all()
    self.assertTrue(pipe_1(data_1))
    self.assertFalse(pipe_1(data_2))

    # causes an error. reported with: https://github.com/BebeSparkelSparkel/functional_pipes/issues/2
    # pipe_2 = pipe_1.same()
    # self.assertEqual(
    #     tuple(val for val, c in zip(pipe_2(iter(data_1)), range(2))),
    #     (True,)
    #   )
    # self.assertEqual(
    #     tuple(val for val, c in zip(pipe_2(iter(data_2)), range(2))),
    #     (True,)
    #   )

  def test_any(self):
    data_1 = 1, 1, 1
    data_2 = 0, 0, 0
    data_3 = ()

    self.assertTrue(Pipe(data_1).any())
    self.assertFalse(Pipe(data_2).any())
    self.assertFalse(Pipe(data_3).any())

    pipe_1 = Pipe().any()
    self.assertTrue(pipe_1(data_1))
    self.assertFalse(pipe_1(data_2))

    # causes an error. reported with: https://github.com/BebeSparkelSparkel/functional_pipes/issues/2
    # pipe_2 = pipe_1.same()
    # self.assertEqual(
    #     tuple(val for val, c in zip(pipe_2(iter(data_1)), range(2))),
    #     (True,)
    #   )
    # self.assertEqual(
    #     tuple(val for val, c in zip(pipe_2(iter(data_2)), range(2))),
    #     (True,)
    #   )

  def test_max_min(self):
    data_1 = 1, 6, 4
    data_1_max = max(data_1)
    data_1_min = min(data_1)
    data_2 = ()

    self.assertEqual(Pipe(data_1).max(), data_1_max)
    self.assertEqual(Pipe(data_1).max(key=lambda a: 1 / a), data_1_min)

    # empty data set
    with self.assertRaises(ValueError):
      Pipe(data_2).max()

    self.assertEqual(Pipe(data_2).max(default=10), 10)

  def test_enumerate(self):
    data_1 = 'a', 'b', 'c'
    data_1_enumerated = tuple(enumerate(data_1))

    self.assertEqual(
        tuple(Pipe(data_1).enumerate()),
        tuple(enumerate(data_1))
      )

    self.assertEqual(
        tuple(Pipe(data_1).enumerate(5)),
        tuple(enumerate(data_1, 5))
      )

  def test_filter_filter_kargs(self):
    data_1 = 1, 2, 3, 4
    func_1 = lambda val: val > 2
    data_2 = (1, 2), (3, 4), (5, 6), (7, 8)
    func_2 = lambda a, b: 2 * a > b and b < 8
    data_3 = tuple(dict(a=v1, b=v2) for v1, v2 in data_2)
    func_3 = func_2

    self.assertEqual(
        tuple(Pipe(data_1).filter(func_1)),
        tuple(filter(func_1, data_1))
      )
    self.assertEqual(
        tuple(Pipe(data_2).filter(func_2)),
        tuple(filter(lambda pair: func_2(*pair), data_2))
      )
    self.assertEqual(
        tuple(Pipe(data_3).filter_kargs(func_3)),
        tuple(filter(lambda kargs: func_3(**kargs), data_3))
      )

  def test_map_map_kargs(self):
    data_1 = 1, 2, 3, 4
    func_1 = lambda val: val > 2
    data_2 = (1, 2), (3, 4), (5, 6), (7, 8)
    func_2 = lambda a, b: 2 * a > b and b < 8
    data_3 = tuple(dict(a=v1, b=v2) for v1, v2 in data_2)
    func_3 = func_2

    self.assertEqual(
        tuple(Pipe(data_1).map(func_1)),
        tuple(map(func_1, data_1))
      )
    self.assertEqual(
        tuple(Pipe(data_2).map(func_2)),
        tuple(map(lambda pair: func_2(*pair), data_2))
      )
    self.assertEqual(
        tuple(Pipe(data_3).map_kargs(func_3)),
        tuple(map(lambda kargs: func_3(**kargs), data_3))
      )

  def test_zip(self):
    data_1 = 1, 2, 3, 4

    self.assertEqual(
        tuple(Pipe(data_1).zip(range(5, 500))),
        tuple(zip(data_1, range(5, 500)))
      )







if __name__ == '__main__':
  unittest.main()