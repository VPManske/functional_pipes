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



if __name__ == '__main__':
  unittest.main()

