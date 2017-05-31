import unittest
from itertools import zip_longest

from pipe_multi import PipeMulti, Confluence


class TestPipeMulti(unittest.TestCase):
  def test_init_iter_call_next(self):
    '''
    test __inti__, __iter__, __call__, __next__.
    No extra methods added.
    '''
    data_1 = 1, 2, 3
    data_2 = 2, 3, 4
    data_3 = 6, 4, 2

    pm_1 = PipeMulti()

    handle_1 = pm_1(data_1)
    handle_2 = pm_1(data_2)

    handle_3 = pm_1()
    handle_3(data_3)

    for h1, d1, h2, d2, h3, d3 in zip_longest(
          handle_1, data_1, handle_2, data_2, handle_3, data_3
        ):
      self.assertEqual(h1, d1)
      self.assertEqual(h2, d2)
      self.assertEqual(h3, d3)


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









