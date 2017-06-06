import unittest, io

from functional_pipes import Pipe
from functional_pipes.built_in_functions import add_class_methods, method_names


class TestMethods(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    add_class_methods(Pipe)

  @classmethod
  def tearDownClass(self):
    for name in method_names:
      delattr(Pipe, name)

  def test_dict(self):
    data_1 = ('a', 1), ('b', 2), ('c', 3)
    data_2 = (1, 2), (3, 4), (5, 6)

    self.assertEqual(
        Pipe(data_1).dict(),
        dict(data_1)
      )

    pipe_1 = Pipe().dict()
    pipe_1(())

    self.assertEqual(
        pipe_1(data_2),
        dict(data_2)
      )

    # with carry_key
    carry_key_pipe = Pipe(
      ).carry_key.map(lambda val: 2 * val
      ).re_key.dict()
    self.assertEqual(
        carry_key_pipe(data_1),
        dict(a=2, b=4, c=6)
      )

  def test_frozenset(self):
    data_1 = 1, 2, 2, 3
    data_2 = (1, 2), (3, 4), (5, 6)

    self.assertEqual(
        Pipe(data_1).frozenset(),
        frozenset(data_1)
      )

    pipe_1 = Pipe().frozenset()
    pipe_1(())

    self.assertEqual(
        pipe_1(data_2),
        frozenset(data_2)
      )

  def test_set(self):
    data_1 = 1, 2, 2, 3, 879, 48, 2
    data_2 = (1, 2), (3, 4), (5, 6)

    self.assertEqual(
        Pipe(data_1).set(),
        set(data_1)
      )

    pipe_1 = Pipe().set()
    pipe_1(())

    self.assertEqual(
        pipe_1(data_2),
        set(data_2)
      )

  def test_list(self):
    data_1 = 1, 2, 2, 3, 879, 48, 2
    data_2 = (1, 2), (3, 4), (5, 6)

    self.assertEqual(
        Pipe(data_1).list(),
        list(data_1)
      )

    pipe_1 = Pipe().list()
    pipe_1(())

    self.assertEqual(
        pipe_1(data_2),
        list(data_2)
      )

  def test_tuple(self):
    data_1 = 1, 2, 2, 3, 879, 48, 2
    data_2 = (1, 2), (3, 4), (5, 6)

    self.assertEqual(
        Pipe(data_1).tuple(),
        tuple(data_1)
      )

    pipe_1 = Pipe().tuple()
    pipe_1(())

    self.assertEqual(
        pipe_1(data_2),
        tuple(data_2)
      )

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
    # Pipe.add_map_method(lambda val: val, 'same')
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
    # Pipe.add_map_method(lambda val: val, 'same')
    # pipe_2 = pipe_1.same()
    # self.assertEqual(
    #     tuple(val for val, c in zip(pipe_2(iter(data_1)), range(2))),
    #     (True,)
    #   )
    # self.assertEqual(
    #     tuple(val for val, c in zip(pipe_2(iter(data_2)), range(2))),
    #     (True,)
    #   )

  def test_max(self):
    data_1 = 1, 6, 4
    data_1_max = max(data_1)
    data_1_min = min(data_1)
    data_2 = ()
    data_3 = ('a', 1), ('b', 2), ('c', 3)
    func_3 = lambda v1, v2: v2
    data_4 = dict(a=1, b=2), dict(a=3, b=4)
    func_4 = lambda a, b: b / a

    # no star function
    self.assertEqual(Pipe(data_1).max(), data_1_max)
    self.assertEqual(Pipe(data_1).max(key=lambda a: 1 / a), data_1_min)

    # empty data set
    with self.assertRaises(ValueError):
      Pipe(data_2).max()

    # default value
    self.assertEqual(Pipe(data_2).max(default=10), 10)

    # star function
    self.assertEqual(
        Pipe(data_3).max(key=func_3),
        max(data_3, key=lambda v: func_3(*v))
      )

    # double star function
    self.assertEqual(
        Pipe(data_4).max_kargs(key=func_4),
        max(data_4, key=lambda v: func_4(**v))
      )


  def test_min(self):
    data_1 = 1, 6, 4
    data_1_min = min(data_1)
    data_1_max = max(data_1)
    data_2 = ()
    data_2 = ()
    data_3 = ('a', 1), ('b', 2), ('c', 3)
    func_3 = lambda v1, v2: v2
    data_4 = dict(a=1, b=2), dict(a=3, b=4)
    func_4 = lambda a, b: b / a

    self.assertEqual(Pipe(data_1).min(), data_1_min)
    self.assertEqual(Pipe(data_1).min(key=lambda a: 1 / a), data_1_max)

    # empty data set
    with self.assertRaises(ValueError):
      Pipe(data_2).min()

    self.assertEqual(Pipe(data_2).min(default=10), 10)

    # star function
    self.assertEqual(
        Pipe(data_3).min(key=func_3),
        min(data_3, key=lambda v: func_3(*v))
      )

    # double star function
    self.assertEqual(
        Pipe(data_4).min_kargs(key=func_4),
        min(data_4, key=lambda v: func_4(**v))
      )

  def test_sum(self):
    data_1 = 1, 2, 3, 4
    data_2 = ()

    self.assertEqual(
        Pipe(data_1).sum(),
        sum(data_1)
      )
    self.assertEqual(
        Pipe(data_1).sum(5),
        sum(data_1, 5)
      )
    self.assertEqual(
        Pipe(data_2).sum(),
        sum(data_2)
      )

  def test_sorted(self):
    data_1 = 1, 2, 2, 3, 879, 48, 2
    data_2 = ('a', 1), ('b', 2), ('c', 3)
    func_2 = lambda a, b: b
    data_3 = dict(a=1, b=2), dict(a=3, b=4)
    func_3 = lambda a, b: 1 / (a * b)

    self.assertEqual(
        Pipe(data_1).sorted(),
        sorted(data_1)
      )
    self.assertEqual(
        Pipe(data_1).sorted(reverse=True),
        sorted(data_1, reverse=True)
      )

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

  # def test_reversed(self):
  #   '''
  #   Not added yet because it requires a sequence
  #   '''
  #   data_1 = 1, 2, 3, 4
  #   data_2 = ()

  #   self.assertEqual(
  #       Pipe(data_1).reversed().tuple(),
  #       tuple(reversed(data_1))
  #     )

  #   self.assertEqual(
  #       Pipe(data_2).reversed().tuple(),
  #       tuple(reversed(data_2))
  #     )


class TestMapMethods(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    add_class_methods(Pipe)

  @classmethod
  def tearDownClass(self):
    for name in method_names:
      delattr(Pipe, name)

  def test_dict_e(self):
    data_1 = (('a', 1), ('b', 2)), (('c', 2), ('d', 3))

    self.assertEqual(
        Pipe(data_1).dict_e().tuple(),
        tuple(dict(kv) for kv in data_1)
      )

  def test_frozenset_e(self):
    data_1 = (2, 4, 6, 3), (1, 2, 2, 5, 5)

    self.assertEqual(
        Pipe(data_1).frozenset_e().tuple(),
        tuple(frozenset(vals) for vals in data_1)
      )

  def test_set_e(self):
    data_1 = (2, 4, 6, 3), (1, 2, 2, 5, 5)

    self.assertEqual(
        Pipe(data_1).set_e().tuple(),
        tuple(set(vals) for vals in data_1)
      )

  def test_list_e(self):
    data_1 = (2, 4, 6, 3), (1, 2, 2, 5, 5)

    self.assertEqual(
        Pipe(data_1).list_e().tuple(),
        tuple(list(vals) for vals in data_1)
      )

  def test_tuple_e(self):
    data_1 = (2, 4, 6, 3), (1, 2, 2, 5, 5)

    self.assertEqual(
        Pipe(data_1).tuple_e().tuple(),
        data_1
      )

  def test_reversed_e(self):
    data_1 = (2, 4, 6, 3), (1, 2, 2, 5, 5)

    self.assertEqual(
        Pipe(data_1).reversed_e().tuple_e().tuple(),
        tuple(tuple(reversed(vals)) for vals in data_1)
      )

  def test_sorted_e(self):
    data_1 = (2, 4, 6, 3), (1, 7, 2, 5, 5)

    self.assertEqual(
        Pipe(data_1).sorted_e().tuple(),
        tuple(sorted(vals) for vals in data_1)
      )

    # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    # self.assertEqual(
    #     Pipe(data_1).sorted_e(reverse=True).tuple(),
    #     tuple(sorted(vals, reverse=True) for vals in data_1)
    #   )

  def test_max_e(self):
    data_1 = (2, 4, 6, 3), (1, 7, 2, 5, 5)

    self.assertEqual(
        Pipe(data_1).max_e().tuple(),
        tuple(max(vals) for vals in data_1)
      )

    # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    # self.assertEqual(
    #     Pipe(data_1).sorted_e(reverse=True).tuple(),
    #     tuple(sorted(vals, reverse=True) for vals in data_1)
    #   )

  def test_min_e(self):
    data_1 = (2, 4, 6, 3), (1, 7, 2, 5, 5)

    self.assertEqual(
        Pipe(data_1).min_e().tuple(),
        tuple(min(vals) for vals in data_1)
      )

    # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    # self.assertEqual(
    #     Pipe(data_1).sorted_e(reverse=True).tuple(),
    #     tuple(sorted(vals, reverse=True) for vals in data_1)
    #   )

  def test_sum_e(self):
    data_1 = (2, 4, 6, 3), (1, 7, 2, 5, 5)

    self.assertEqual(
        Pipe(data_1).sum_e().tuple(),
        tuple(sum(vals) for vals in data_1)
      )

    # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    # self.assertEqual(
    #     Pipe(data_1).sorted_e(reverse=True).tuple(),
    #     tuple(sorted(vals, reverse=True) for vals in data_1)
    #   )

  def test_str(self):
    data_1 = (2, 4, 6, 3), (1, 2, 2, 5, 5)

    self.assertEqual(
        Pipe(data_1).str().tuple(),
        tuple(str(vals) for vals in data_1)
      )

    # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    # for encoding and errors arguments

  def test_ascii(self):
    data_1 = -1, 2, -3, 4

    self.assertEqual(
        Pipe(data_1).ascii().tuple(),
        tuple(ascii(d) for d in data_1)
      )

  def test_bin(self):
    data_1 = -1, 2, -3, 4

    self.assertEqual(
        Pipe(data_1).bin().tuple(),
        tuple(bin(d) for d in data_1)
      )

  def test_bool(self):
    data_1 = -1, 0, -3, 4

    self.assertEqual(
        Pipe(data_1).bool().tuple(),
        tuple(bool(d) for d in data_1)
      )

  def test_callable(self):
    data_1 = -1, map, -3, str

    self.assertEqual(
        Pipe(data_1).callable().tuple(),
        tuple(callable(d) for d in data_1)
      )

  def test_chr(self):
    data_1 = 3, 39, 55

    self.assertEqual(
        Pipe(data_1).chr().tuple(),
        tuple(chr(d) for d in data_1)
      )

  def test_classmethod(self):
    data_1 = -1, map, -3, str

    for cm in Pipe(data_1).classmethod():
      self.assertTrue(isinstance(cm, classmethod))

  def test_staticmethod(self):
    data_1 = -1, map, -3, str

    for cm in Pipe(data_1).staticmethod():
      self.assertTrue(isinstance(cm, staticmethod))

  def test_eval(self):
    # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    data_1 = '5 + 4', '"hi" + "there"'

    self.assertEqual(
        Pipe(data_1).eval().tuple(),
        tuple(eval(d) for d in data_1)
      )

  def test_float(self):
    data_1 = 3, 39, 55, '-44'

    self.assertEqual(
        Pipe(data_1).float().tuple(),
        tuple(float(d) for d in data_1)
      )

  def test_hash(self):
    data_1 = 3, 39, 55, '-44'

    self.assertEqual(
        Pipe(data_1).hash().tuple(),
        tuple(hash(d) for d in data_1)
      )

  def test_hex(self):
    data_1 = 3, 39, 55

    self.assertEqual(
        Pipe(data_1).hex().tuple(),
        tuple(hex(d) for d in data_1)
      )

  def test_id(self):
    data_1 = 3, 39, 55, '-44'

    self.assertEqual(
        Pipe(data_1).id().tuple(),
        tuple(id(d) for d in data_1)
      )

  def test_int(self):
    # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    data_1 = 3, 39.0, 55, '-44'

    self.assertEqual(
        Pipe(data_1).int().tuple(),
        tuple(int(d) for d in data_1)
      )

  def test_iter(self):
    # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    data_1 = (2, 4, 6, 3), (1, 2, 2, 5, 5)

    self.assertEqual(
        Pipe(data_1).iter().tuple_e().tuple(),
        data_1
      )

  def test_len(self):
    data_1 = (2, 4, 6, 3), (1, 2, 2, 5, 5)

    self.assertEqual(
        Pipe(data_1).len().tuple(),
        tuple(len(vals) for vals in data_1)
      )

  def test_oct(self):
    data_1 = 3, 39, 55

    self.assertEqual(
        Pipe(data_1).oct().tuple(),
        tuple(oct(d) for d in data_1)
      )

  # def test_open(self):
  #   # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
  #   data_1 = 'test_pipe.py', 'test_pipe_multi.py'

  #   for fs in Pipe(data_1).open():
  #     self.assertTrue(isinstance(fs, io.TextIOWrapper))
  #     fs.close()

  def test_ord(self):
    data_1 = 'abced45'

    self.assertEqual(
        Pipe(data_1).ord().tuple(),
        tuple(ord(d) for d in data_1)
      )

  def test_range(self):
    data_1 = 1, 2, 4

    self.assertEqual(
        Pipe(data_1).range().tuple(),
        tuple(range(d) for d in data_1)
      )

  def test_repr(self):
    data_1 = 1, 2, 4

    self.assertEqual(
        Pipe(data_1).repr().tuple(),
        tuple(repr(d) for d in data_1)
      )

  def test_round(self):
    data_1 = 1.4, 2.6, 4.3

    self.assertEqual(
        Pipe(data_1).round().tuple(),
        tuple(round(d) for d in data_1)
      )

  def test_type(self):
    # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    data_1 = 1.4, '2.6', map

    self.assertEqual(
        Pipe(data_1).type().tuple(),
        tuple(type(d) for d in data_1)
      )

class TestKeyMapMethods(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    add_class_methods(Pipe)

  @classmethod
  def tearDownClass(self):
    for name in method_names:
      delattr(Pipe, name)

  def test_dict_e_keyed(self):
    data_1 = (('a', 1), ('b', 2)), (('c', 2), ('d', 3))

    self.assertEqual(
        Pipe(data_1).dict_e_keyed().tuple(),
        tuple((kv, dict(kv)) for kv in data_1)
      )

  def test_frozenset_e_keyed(self):
    data_1 = (2, 4, 6, 3), (1, 2, 2, 5, 5)

    self.assertEqual(
        Pipe(data_1).frozenset_e_keyed().tuple(),
        tuple((vals, frozenset(vals)) for vals in data_1)
      )

  def test_set_e_keyed(self):
    data_1 = (2, 4, 6, 3), (1, 2, 2, 5, 5)

    self.assertEqual(
        Pipe(data_1).set_e_keyed().tuple(),
        tuple((vals, set(vals)) for vals in data_1)
      )

  def test_list_e_keyed(self):
    data_1 = (2, 4, 6, 3), (1, 2, 2, 5, 5)

    self.assertEqual(
        Pipe(data_1).list_e_keyed().tuple(),
        tuple((vals, list(vals)) for vals in data_1)
      )

  def test_tuple_e_keyed(self):
    data_1 = (2, 4, 6, 3), (1, 2, 2, 5, 5)

    self.assertEqual(
        Pipe(data_1).tuple_e_keyed().tuple(),
        tuple(zip(data_1, data_1))
      )

  def test_reversed_e_keyed(self):
    data_1 = (2, 4, 6, 3), (1, 2, 2, 5, 5)

    self.assertEqual(
        Pipe(data_1
          ).reversed_e_keyed(
          ).map(lambda key, val: (key, tuple(val))
          ).tuple(),
        tuple((vals, tuple(reversed(vals))) for vals in data_1)
      )

  def test_sorted_e_keyed(self):
    data_1 = (2, 4, 6, 3), (1, 7, 2, 5, 5)

    self.assertEqual(
        Pipe(data_1).sorted_e_keyed().tuple(),
        tuple((vals, sorted(vals)) for vals in data_1)
      )

    # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    # self.assertEqual(
    #     Pipe(data_1).sorted_e(reverse=True).tuple(),
    #     tuple(sorted(vals, reverse=True) for vals in data_1)
    #   )

  def test_max_e_keyed(self):
    data_1 = (2, 4, 6, 3), (1, 7, 2, 5, 5)

    self.assertEqual(
        Pipe(data_1).max_e_keyed().tuple(),
        tuple((vals, max(vals)) for vals in data_1)
      )

    # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    # self.assertEqual(
    #     Pipe(data_1).sorted_e(reverse=True).tuple(),
    #     tuple(sorted(vals, reverse=True) for vals in data_1)
    #   )

  def test_min_e_keyed(self):
    data_1 = (2, 4, 6, 3), (1, 7, 2, 5, 5)

    self.assertEqual(
        Pipe(data_1).min_e_keyed().tuple(),
        tuple((vals, min(vals)) for vals in data_1)
      )

    # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    # self.assertEqual(
    #     Pipe(data_1).sorted_e(reverse=True).tuple(),
    #     tuple(sorted(vals, reverse=True) for vals in data_1)
    #   )

  def test_sum_e_keyed(self):
    data_1 = (2, 4, 6, 3), (1, 7, 2, 5, 5)

    self.assertEqual(
        Pipe(data_1).sum_e_keyed().tuple(),
        tuple((vals, sum(vals)) for vals in data_1)
      )

    # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    # self.assertEqual(
    #     Pipe(data_1).sorted_e(reverse=True).tuple(),
    #     tuple(sorted(vals, reverse=True) for vals in data_1)
    #   )

  def test_str_keyed(self):
    data_1 = (2, 4, 6, 3), (1, 2, 2, 5, 5)

    self.assertEqual(
        Pipe(data_1).str_keyed().tuple(),
        tuple((vals, str(vals)) for vals in data_1)
      )

    # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    # for encoding and errors arguments

  def test_ascii_keyed(self):
    data_1 = -1, 2, -3, 4

    self.assertEqual(
        Pipe(data_1).ascii_keyed().tuple(),
        tuple((d, ascii(d)) for d in data_1)
      )

  def test_bin_keyed(self):
    data_1 = -1, 2, -3, 4

    self.assertEqual(
        Pipe(data_1).bin_keyed().tuple(),
        tuple((d, bin(d)) for d in data_1)
      )

  def test_bool_keyed(self):
    data_1 = -1, 0, -3, 4

    self.assertEqual(
        Pipe(data_1).bool_keyed().tuple(),
        tuple((d, bool(d)) for d in data_1)
      )

  def test_callable_keyed(self):
    data_1 = -1, map, -3, str

    self.assertEqual(
        Pipe(data_1).callable_keyed().tuple(),
        tuple((d, callable(d)) for d in data_1)
      )

  def test_chr_keyed(self):
    data_1 = 3, 39, 55

    self.assertEqual(
        Pipe(data_1).chr_keyed().tuple(),
        tuple((d, chr(d)) for d in data_1)
      )

  def test_classmethod_keyed(self):
    data_1 = -1, map, -3, str

    for obj, cm in Pipe(data_1).classmethod_keyed():
      self.assertTrue(isinstance(cm, classmethod))

  def test_staticmethod_keyed(self):
    data_1 = -1, map, -3, str

    for obj, cm in Pipe(data_1).staticmethod_keyed():
      self.assertTrue(isinstance(cm, staticmethod))

  def test_eval_keyed(self):
    # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    data_1 = '5 + 4', '"hi" + "there"'

    self.assertEqual(
        Pipe(data_1).eval_keyed().tuple(),
        tuple((d, eval(d)) for d in data_1)
      )

  def test_float_keyed(self):
    data_1 = 3, 39, 55, '-44'

    self.assertEqual(
        Pipe(data_1).float_keyed().tuple(),
        tuple((d, float(d)) for d in data_1)
      )

  def test_hash_keyed(self):
    data_1 = 3, 39, 55, '-44'

    self.assertEqual(
        Pipe(data_1).hash_keyed().tuple(),
        tuple((d, hash(d)) for d in data_1)
      )

  def test_hex_keyed(self):
    data_1 = 3, 39, 55

    self.assertEqual(
        Pipe(data_1).hex_keyed().tuple(),
        tuple((d, hex(d)) for d in data_1)
      )

  def test_id_keyed(self):
    data_1 = 3, 39, 55, '-44'

    self.assertEqual(
        Pipe(data_1).id_keyed().tuple(),
        tuple((d, id(d)) for d in data_1)
      )

  def test_int_keyed(self):
    # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    data_1 = 3, 39.0, 55, '-44'

    self.assertEqual(
        Pipe(data_1).int_keyed().tuple(),
        tuple((d, int(d)) for d in data_1)
      )

  def test_iter_keyed(self):
    # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    data_1 = (2, 4, 6, 3), (1, 2, 2, 5, 5)
    tuple_iterator = type(iter(data_1))

    self.assertTrue(
        Pipe(data_1).iter_keyed(
          ).map(lambda key, val: val
          ).type(
          ).map(lambda t: str(t) == str(tuple_iterator)
          ).all()
        )

  def test_len_keyed(self):
    data_1 = (2, 4, 6, 3), (1, 2, 2, 5, 5)

    self.assertEqual(
        Pipe(data_1).len_keyed().tuple(),
        tuple((vals, len(vals)) for vals in data_1)
      )

  def test_oct_keyed(self):
    data_1 = 3, 39, 55

    self.assertEqual(
        Pipe(data_1).oct_keyed().tuple(),
        tuple((d, oct(d)) for d in data_1)
      )

  # def test_open_keyed(self):
  #   # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
  #   data_1 = 'test_pipe.py', 'test_pipe_multi.py'
  #   data_1_iter = iter(data_1)

  #   for path, fs in Pipe(data_1).open_keyed():
  #     self.assertEqual(path, next(data_1_iter))
  #     self.assertTrue(isinstance(fs, io.TextIOWrapper))
  #     fs.close()

  def test_ord_keyed(self):
    data_1 = 'abced45'

    self.assertEqual(
        Pipe(data_1).ord_keyed().tuple(),
        tuple((d, ord(d)) for d in data_1)
      )

  def test_range_keyed(self):
    data_1 = 1, 2, 4

    self.assertEqual(
        Pipe(data_1).range_keyed().tuple(),
        tuple((d, range(d) )for d in data_1)
      )

  def test_repr_keyed(self):
    data_1 = 1, 2, 4

    self.assertEqual(
        Pipe(data_1).repr_keyed().tuple(),
        tuple((d, repr(d)) for d in data_1)
      )

  def test_round_keyed(self):
    data_1 = 1.4, 2.6, 4.3

    self.assertEqual(
        Pipe(data_1).round_keyed().tuple(),
        tuple((d, round(d)) for d in data_1)
      )

  def test_type_keyed(self):
    # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    data_1 = 1.4, '2.6', map

    self.assertEqual(
        Pipe(data_1).type_keyed().tuple(),
        tuple((d, type(d)) for d in data_1)
      )


if __name__ == '__main__':
  unittest.main()