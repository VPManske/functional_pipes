import operator as o

from collections import ChainMap


def add_class_methods(pipe_class):
    # map methods
    for func_properties in map_methods_to_add:
      if isinstance(func_properties, dict):
        name = pipe_class.add_map_method(**func_properties)
      else:
        name = pipe_class.add_map_method(func_properties)

      method_names.add(name)

    # key map methods
    for func_properties in map_methods_to_add:
      if isinstance(func_properties, dict):
        name = pipe_class.add_key_map_method(**ChainMap(
            dict(func_name=func_properties['func_name'] + '_keyed'),
            func_properties
          ))
      else:
        name = pipe_class.add_key_map_method(
            func = func_properties,
            func_name = func_properties.__name__ + '_keyed',
          )

      method_names.add(name)


method_names = set() # holds all the method names that were added to Pipe


map_methods_to_add = (
    o.add,
    o.mul,
  )