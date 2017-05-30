import unittest
from itertools import zip_longest

from support import Reservoir, Valve, ResHandle, Confluence

# class TestValve(unittest.TestCase):
#   def test_iterable_object(self):
#     '''
#     tests functions that return an iterable object
#     using sorted because it returns an iterable object
#     '''
#     test_function = sorted

#     data_1 = 2, 1, 3
#     data_2 = 5, 2, 6, 7, 2, 4, 6

#     # test reuse with Reservoir
#     resv_3 = Reservoir(data_1)
#     valve_3 = Valve(func=test_function, pass_args=(resv_3,))
#     self.assertTrue(list(valve_3), sorted(data_1))
#     with self.assertRaises(StopIteration):
#       next(valve_3)
#     resv_3(data_2)
#     self.assertTrue(next(valve_3), sorted(data_2))

#     print()
#     valve_4 = Valve(func=test_function, pass_args=(data_1,))
#     self.assertIs(next(valve_4), sorted(data_1)[0])
#     for f, d in zip_longest(valve_4, sorted(data_1)[1:]):
#       print('f', f, 'd', d)
#       self.assertIs(f, d)
#     print()

#     # pass in a karg with pass_kargs
#     valve_5 = Valve(
#         func=test_function,
#         pass_args=(iter(data_1),),
#         pass_kargs=dict(reverse=True),
#       )
#     self.assertEqual(list(valve_5), sorted(data_1, reverse=True))
#     with self.assertRaises(StopIteration):
#       next(valve_5)

#   def test_non_iterable_object(self):
#     '''
#     tests functions that return a non iterable object
#     using max because it returns a non iterable object
#     '''
#     test_function = max

#     data_1 = 2, 1, 3
#     max_1 = test_function(data_1)
#     data_2 = 5, 2, 6, 7, 2, 4, 6
#     max_2 = test_function(data_2)

#     valve_1 = Valve(
#         func = test_function,
#         pass_args = (iter(data_1),),
#         empty_error = ValueError,
#       )
#     result_1 = next(valve_1)
#     self.assertIs(result_1, max_1)
#     with self.assertRaises(StopIteration):
#       next(valve_1)

#     # test with reservoir
#     resr_2 = Reservoir(data_1)
#     valve_2 = Valve(func=test_function, pass_args=(resr_2,), empty_error=ValueError)
#     self.assertIs(next(valve_2), max_1)
#     with self.assertRaises(StopIteration):
#       next(valve_2)
#     resr_2(data_2)
#     self.assertIs(next(valve_2), max_2)


# class TestReservoir(unittest.TestCase):
#   def test_init(self):
#     Reservoir()

#     data_1 = 1, 2, 3, 4
#     sp1 = Reservoir(data_1)
#     self.assertEqual(tuple(sp1.iterator), data_1)

#     sp2 = Reservoir(data_1)
#     self.assertIsNot(sp1, sp2)

#   def test_iter_next_call(self):
#     # test iter and next
#     sp1 = Reservoir()

#     with self.assertRaises(StopIteration):
#       next(sp1)

#     data_1 = tuple(range(10))
#     sp1(range(10))

#     for s, d in zip_longest(sp1, data_1):
#       self.assertEqual(s, d)


#     # test call
#     sp2 = Reservoir()

#     with self.assertRaises(TypeError):
#       next(sp2.iterator)

#     # first fill
#     data_1 = 1, 2, 3
#     sp2(data_1)
#     self.assertEqual(tuple(sp2), data_1)

#     # second fill
#     data_2 = 4, 5, 6
#     sp2(data_2)
#     self.assertEqual(tuple(sp2), data_2)

#     # call when reservoir not yet empty
#     sp2(data_1)
#     with self.assertRaises(ValueError):
#       sp2(data_1)

#   def test_drain_then_fill(self):
#     data_1 = 1, 2, 4, 8
#     data_2 = 5, 3, 6, 9

#     r1 = Reservoir(data_1)
#     tuple(r1)
#     r1(data_2)


class TestConfluence(unittest.TestCase):
  # def test_handles(self):
  #   data_1 = 1, 2, 4, 8
  #   data_2 = 5, 3, 6, 9

  #   c1 = Confluence()

  #   # test a single flow
  #   self.assertEqual(
  #       tuple(c1.new_handle(data_1)),
  #       data_1
  #     )

  #   # test mutiple flows
  #   handle_1 = c1.new_handle(data_1)
  #   handle_2 = c1.new_handle(data_2)

  #   for h1, h2, d1, d2 in zip_longest(handle_1, handle_2, data_1, data_2):
  #     self.assertIs(h1, d1)
  #     self.assertIs(h2, d2)

  #   with self.assertRaises(StopIteration):
  #     next(handle_1)
  #   with self.assertRaises(StopIteration):
  #     next(handle_2)

  #   handle_2(data_1)
  #   self.assertEqual(
  #       tuple(handle_2),
  #       data_1
  #     )

  def test_res_not_filling(self):
    '''
    After pulling data from multiple streams with tuple then tried to refill the
    stream but an error is thrown that the reservoirs isn't empty.
    '''
    data_1 = 1, 2, 4, 8

    c1 = Confluence()
    handle_1 = c1.new_handle(data_1)
    handle_2 = c1.new_handle(data_1)
    for h1, h2, d1, d2 in zip(handle_1, handle_2, data_1, data_2):
      pass

    handle_1(data_1)
    handle_2(data_1)













if __name__ == '__main__':
  unittest.main()









