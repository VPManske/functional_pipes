import functional_pipes as fp
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


def dict_zip(iterable):
  '''
  Yields a dictionary with the same keys that dict_w_iter has.
  The values are all of the same index from the iterator from the
  values from dict_w_iter.

  Example:
  >>> data_dict = dict(
  ...    a = (1,2,3),
  ...    b = (4,5,6),
  ...  )
  ...
  >>> for row in dict_zip(data_dict):
  ...  print(row)
  ...
  {'a': 1, 'b': 4}
  {'a': 2, 'b': 5}
  {'a': 3, 'b': 6}
  '''
  for dict_w_iter in iterable:
    lables = dict_w_iter.keys()
    matrix = tuple(dict_w_iter[k] for k in lables)
    for row in zip(*matrix):
      yield dict(zip(lables, row))


# profile methods to add
methods_to_add = (
    wrap_gener(zip_internal),
    wrap_gener(dict_zip),
  )

for method_properties in methods_to_add:
  if isinstance(method_properties, dict):
    fp.Pipe.add_method(**method_properties)
  else:
    fp.Pipe.add_method(method_properties)

