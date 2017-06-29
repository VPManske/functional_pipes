'''
methods that come from python's itertools package
'''

import itertools as it


def groupby_key(iterable):
  return it.groupby(iterable, lambda key_val: key_val[0])


# methods
methods_to_add = (
    it.groupby,
    groupby_key,
  )


# map methods
map_methods_to_add = (
  )
