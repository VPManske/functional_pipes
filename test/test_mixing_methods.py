'''
Tests if importing methods from multiple definition files adds all methods to Pipe
'''

import unittest
from itertools import chain

from functional_pipes import Pipe, built_in_functions, custom_pipes, testing_tools


class TestMix(unittest.TestCase):
  @classmethod
  def setUpClass(self):
    built_in_functions.add_class_methods(Pipe)
    custom_pipes.add_class_methods(Pipe)
    testing_tools.add_class_methods(Pipe)

  @classmethod
  def tearDownClass(self):
    method_names = chain(*(package.method_names for package in (
        built_in_functions,
        custom_pipes,
        testing_tools,
      )))

    for name in method_names:
      delattr(Pipe, name)

  def test_mix(self):
    method_names = chain(*(package.method_names for package in (
        built_in_functions,
        custom_pipes,
        testing_tools,
      )))

    for method in method_names:
      self.assertTrue(hasattr(Pipe, method))


if __name__ == '__main__':
  unittest.main()

