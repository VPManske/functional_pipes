import itertools as it

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
methods_to_add = (
    dict(gener=it.groupby, is_valve=True, star_wrap=1),
  )


# map methods
map_methods_to_add = (
  )
