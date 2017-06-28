import unittest, io
from itertools import chain

from functional_pipes import Pipe


class TestMethods(unittest.TestCase):
  @classmethod
  def setUpClass(self):
    Pipe.load('built_in_functions')

  @classmethod
  def tearDownClass(self):
    Pipe.unload('built_in_functions')

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

  def test_flatten(self):
    data = (1, 2), (3, 4, 5)
    ref = 1, 2, 3, 4, 5

    self.assertEqual(
        Pipe(data).flatten().tuple(),
        ref
      )

    pipe_empty = Pipe().flatten().tuple()
    self.assertEqual(pipe_empty(data), ref)
    self.assertEqual(pipe_empty(data), ref) # reload the pipe

  def test_drop_key(self):
    data = (1, 2), (3, 4), (5, 6)
    ref = 2, 4, 6

    self.assertEqual(
        Pipe(data).drop_key.tuple(),
        ref
      )

    pipe_reuse = Pipe().drop_key.tuple()
    self.assertEqual(pipe_reuse(data), ref)
    self.assertEqual(pipe_reuse(data), ref) # reload the pipe

  def test_grab_with_tuple(self):
    data = (1, 2), (3, 4), (5, 6)
    ref = 2, 4, 6

    self.assertEqual(
        Pipe(data).grab[1].tuple(),
        ref
      )

    pipe_reuse = Pipe().grab[1].tuple()
    self.assertEqual(pipe_reuse(data), ref)
    self.assertEqual(pipe_reuse(data), ref) # reload the pipe

  def test_grab_with_dict(self):
    data = (1, 2), (3, 4), (5, 6)
    data = (dict(a=a, b=b) for a, b in data)
    ref = 2, 4, 6

    print()
    print(Pipe().grab)
    print()
    return

    self.assertEqual(
        Pipe(data).grab['b'].tuple(),
        ref
      )

    pipe_reuse = Pipe().grab['b'].tuple()
    self.assertEqual(pipe_reuse(data), ref)
    self.assertEqual(pipe_reuse(data), ref) # reload the pipe



if __name__ == '__main__':
  unittest.main()

