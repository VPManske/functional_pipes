'''
These methods are loaded automatically because they are inherent methods for using
pipes.
'''
from functional_pipes.wrap_gener import wrap_gener


# definitions for methods

def flatten(iterable):
  '''
  expands the items in iterable and yields one at a time

  Example:
  >>> data = [(1, 2), (3, 4, 5)]
  >>> Pipe(data).flatten().tuple()
  (1, 2, 3, 4, 5)
  '''
  for elements in iterable:
    for ele in elements:
      yield ele


methods_to_add = (
    wrap_gener(flatten),
  )


# definitions for map methods

def drop_key(key_val):
  return key_val[1]


map_methods_to_add = (
    dict(func=drop_key, as_property=True),
  )