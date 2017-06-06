from functional_pipes.wrap_gener import wrap_gener


def add_class_methods(pipe_class):
  # methods
  for method_properties in methods_to_add:
    if isinstance(method_properties, dict):
      name = pipe_class.add_method(**method_properties)

    else:
      name = pipe_class.add_method(method_properties)

    method_names.add(name)


method_names = set() # holds all the method names that were added to Pipe


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


# profile methods to add
methods_to_add = (
    wrap_gener(zip_internal),
    wrap_gener(zip_to_dict),
  )

