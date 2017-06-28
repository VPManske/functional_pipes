'''
custom methods that are not other libraries
'''

from functional_pipes.wrap_gener import wrap_gener


# define functions
def zip_internal(iterable):
  '''
  Zips all objects from iterable together.

  Example:
  >>> data_1 = (1, 2, 3), (4, 5, 6), (7, 8, 9)
  >>> Pipe(data_1).zip_internal().tuple()
  ((1, 4, 7), (2, 5, 8), (3, 6, 9))
  '''
  for zipped in zip(*iterable):
    yield zipped


def zip_to_dict(iterable):
  '''
  yields a dict with keys and the corrisponding next value

  iterable - (key, value) tuple pairs. value must be iterable

  Example:
  >>> data = ('a', (1, 2)), ('b', (3, 4))
  >>> Pipe(data).zip_to_dict().tuple()
  ({'a': 1, 'b': 3}, {'a': 2, 'b': 4})
  '''
  stored = tuple((key, iter(value)) for key, value in iterable)

  while stored:
    try:
      yield {key: next(iter_val) for key, iter_val in stored}
    except StopIteration:
      break


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


# profile methods to add
methods_to_add = (
    wrap_gener(zip_internal),
    wrap_gener(zip_to_dict),
    wrap_gener(flatten),
  )


map_methods_to_add = ()
