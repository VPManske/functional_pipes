from collections import ChainMap

import functional_pipes as fp


method_names = [] # holds all the method names that were added to Pipe


methods_to_add = (
    # collection
    dict(gener=dict, is_valve=True),
    dict(gener=frozenset, is_valve=True),
    dict(gener=set, is_valve=True),
    dict(gener=list, is_valve=True),
    dict(gener=tuple, is_valve=True),

    # non iterable valves
    dict(gener=all, is_valve=True),
    dict(gener=any, is_valve=True),
    dict(gener=max, is_valve=True, star_wrap='key', empty_error=ValueError),  # https://github.com/BebeSparkelSparkel/functional_pipes/issues/3
    dict(gener=min, is_valve=True, star_wrap='key', empty_error=ValueError),  # https://github.com/BebeSparkelSparkel/functional_pipes/issues/3
    dict(gener=max, gener_name='max_kargs', is_valve=True, double_star_wrap='key', empty_error=ValueError),  # https://github.com/BebeSparkelSparkel/functional_pipes/issues/3
    dict(gener=min, gener_name='min_kargs', is_valve=True, double_star_wrap='key', empty_error=ValueError),  # https://github.com/BebeSparkelSparkel/functional_pipes/issues/3
    dict(gener=sum, is_valve=True),

    # iterable valves
    dict(gener=sorted, is_valve=True, star_wrap='key'),  # https://github.com/BebeSparkelSparkel/functional_pipes/issues/3
    dict(gener=sorted, gener_name='sorted_kargs', is_valve=True, double_star_wrap='key'),  # https://github.com/BebeSparkelSparkel/functional_pipes/issues/3

    # non valve functions
    dict(gener=enumerate),
    dict(gener=filter, iter_index=1, star_wrap=0),  # https://github.com/BebeSparkelSparkel/functional_pipes/issues/3
    dict(gener=filter, gener_name='filter_kargs', iter_index=1, double_star_wrap=0),  # https://github.com/BebeSparkelSparkel/functional_pipes/issues/3
    dict(gener=map, iter_index=1, star_wrap=0),
    dict(gener=map, gener_name='map_kargs', iter_index=1, double_star_wrap=0),
    dict(gener=zip),
  )

for method_properties in methods_to_add:
  name = fp.Pipe.add_method(**method_properties)
  method_names.append(name)


map_methods_to_add = (
    dict(func=dict, func_name='dict_e'),
    dict(func=frozenset, func_name='frozenset_e'),
    dict(func=set, func_name='set_e'),
    dict(func=list, func_name='list_e'),
    dict(func=tuple, func_name='tuple_e'),
    dict(func=reversed, func_name='reversed_e'),

    dict(func=sorted, func_name='sorted_e'), # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    dict(func=max, func_name='max_e'), # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    dict(func=min, func_name='min_e'), # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    dict(func=sum, func_name='sum_e'), # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4

    str,
    abs,
    ascii,
    bin,
    bool,
    callable,
    chr,
    classmethod,
    staticmethod,
    # complex,  # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    # divmod,  # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    eval,  # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    float,
    # format,  # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    # getattr(object, name[, default]),  # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    # hasattr(object, name),  # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    hash,
    hex,
    id,
    int,  # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    # isinstance,  # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    # issubclass,  # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    iter,  # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    len,
    oct,
    open,  # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    ord,
    # pow,  # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    # property,  # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    range,  # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    repr,
    round, # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    # super,  # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    type,  # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
  )

for func_properties in map_methods_to_add:
  if isinstance(func_properties, dict):
    name = fp.Pipe.add_map_method(**func_properties)
  else:
    name = fp.Pipe.add_map_method(func_properties)

  method_names.append(name)

# key map methods
for func_properties in map_methods_to_add:
  if isinstance(func_properties, dict):
    name = fp.Pipe.add_key_map_method(**ChainMap(
        dict(func_name=func_properties['func_name'] + '_keyed'),
        func_properties
      ))
  else:
    name = fp.Pipe.add_key_map_method(
        func = func_properties,
        func_name = func_properties.__name__ + '_keyed',
      )

  method_names.append(name)

# func, func_name=None, no_over_write=True