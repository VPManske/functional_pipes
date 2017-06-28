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


class grab:
  '''
  allows the dict to bypass one pipe segment
  '''
  def __init__(self, pipe):
    self.pipe = pipe

  def __getitem__(self, key):
    '''
    self - pipe instance
    key - the index key for each element that passes through
    '''

    return self.pipe.map(lambda indexable: indexable[key])


methods_to_add = (
    dict(gener=map, iter_index=1, star_wrap=0),
    dict(gener=map, gener_name='map_kargs', iter_index=1, double_star_wrap=0),
    wrap_gener(flatten),
    dict(gener=grab, as_property=True),
  )


# definitions for map methods

def drop_key(key_val):
  '''
  drops the key in the key value pairs

  Ex: ((1, 2), (3, 4), (5, 6)) => (2, 4, 6)
  '''
  return key_val[1]


map_methods_to_add = (
    dict(func=drop_key, as_property=True),
  )