import unittest
from itertools import zip_longest

from pipe_multi import Confluence


class TestConfluence(unittest.TestCase):
  def test_handles(self):
    data_1 = 1, 2, 4, 8
    data_2 = 5, 3, 6, 9

    c1 = Confluence()

    # test a single flow
    self.assertEqual(
        tuple(c1.new_handle(data_1)),
        data_1
      )

    # test mutiple flows
    handle_1 = c1.new_handle(data_1)
    handle_2 = c1.new_handle(data_2)

    for h1, h2, d1, d2 in zip_longest(handle_1, handle_2, data_1, data_2):
      self.assertIs(h1, d1)
      self.assertIs(h2, d2)

    with self.assertRaises(StopIteration):
      next(handle_1)
    with self.assertRaises(StopIteration):
      next(handle_2)

    handle_2(data_1)
    self.assertEqual(
        tuple(handle_2),
        data_1
      )

  def test_res_not_filling(self):
    '''
    After pulling data from multiple streams with tuple then tried to refill the
    stream but an error is thrown that the reservoirs isn't empty.
    '''
    data_1 = 1, 2, 4, 8

    c1 = Confluence()
    handle_1 = c1.new_handle(data_1)

    for vals in zip(range(len(data_1)), handle_1):
      pass

    handle_1(data_1)














if __name__ == '__main__':
  unittest.main()









