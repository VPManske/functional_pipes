'''
tests if add-ins can be loaded and unloaded as methods for the pipe class
'''

import unittest

from functional_pipes import Pipe
import functional_pipes.add_ins.built_in_functions as built_in_functions
import functional_pipes.add_ins.itertools_pipes as itertools_pipes


class TestLoad(unittest.TestCase):
  def test_load_unload(self):
    Pipe.load('built_in_functions', 'itertools_pipes')

    def get_name(method):
      '''
      returns the name that the method has been added to Pipe as
      '''
      if isinstance(method, dict):
        if 'name' in method:
          name = method['name']
        elif 'gener' in method:
          name = method['gener'].__name__
        elif 'func' in method:
          name = method['func'].__name__
        else:
          raise ValueError('method name cannot be found.')

      else:
        name = method.__name__

      return name

    methods = tuple(
        get_name(method)
        for add_in in (built_in_functions, itertools_pipes)
        for collection in ('methods_to_add', 'map_methods_to_add')
        for method in getattr(add_in, collection)
      )

    self.assertTrue(all(
        hasattr(Pipe, name) for name in methods
      ))

    # check unloading
    with self.assertRaises(KeyError):
      Pipe.unload('not an add-in')

    Pipe.unload('built_in_functions', 'itertools_pipes')

    self.assertFalse(any(
        hasattr(Pipe, name) for name in methods
      ))

    self.assertFalse(hasattr(Pipe, 'dict'))




