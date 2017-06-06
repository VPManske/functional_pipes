def add_class_methods(pipe_class):
  # methods
  for method_properties in methods_to_add:
    if isinstance(method_properties, dict):
      name = pipe_class.add_method(**method_properties)

    else:
      name = pipe_class.add_method(method_properties)

    method_names.add(name)

  # map methods
  for func_properties in map_methods_to_add:
    if isinstance(func_properties, dict):
      name = pipe_class.add_map_method(**func_properties)
    else:
      name = pipe_class.add_map_method(func_properties)

    method_names.add(name)


method_names = set() # holds all the method names that were added to Pipe


# methods

def limit_size(iterable, max_size, label=''):
  '''
  Limits the number of objects passed through the pipe segment to max_size.
  If more objects are passed through then a ValueError is raised.

  iterable - object with next method
  max_size - maximum number of object that will be passed through
  label - if more than one limit size is defined then a label can be passed
    defined to give more specifec error reports
  '''
  def raise_if_larger(size_and_pass):
    if size_and_pass[0] >= max_size:
      raise ValueError('More objects passed through limit_size {} than {}'
        .format(label, max_size))
    return size_and_pass[1]

  return map(raise_if_larger, enumerate(iterable))

methods_to_add = (
    limit_size,
  )


# map methods

def look_in(pass_through, to_append):
  '''
  Appends pass_through to to_append and returns pass_through.
  Good for checking on the values at a set location in a pipe.
  '''
  to_append.append(pass_through)
  return pass_through


map_methods_to_add = (
    look_in,
  )
