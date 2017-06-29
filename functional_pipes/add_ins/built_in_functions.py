'''
Methods that come from python's built in functions
'''

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
    dict(gener=max, name='max_kargs', is_valve=True, double_star_wrap='key', empty_error=ValueError),  # https://github.com/BebeSparkelSparkel/functional_pipes/issues/3
    dict(gener=min, name='min_kargs', is_valve=True, double_star_wrap='key', empty_error=ValueError),  # https://github.com/BebeSparkelSparkel/functional_pipes/issues/3
    dict(gener=sum, is_valve=True),

    # iterable valves
    dict(gener=sorted, is_valve=True, star_wrap='key'),  # https://github.com/BebeSparkelSparkel/functional_pipes/issues/3
    dict(gener=sorted, name='sorted_kargs', is_valve=True, double_star_wrap='key'),  # https://github.com/BebeSparkelSparkel/functional_pipes/issues/3

    # non valve functions
    dict(gener=enumerate),
    dict(gener=filter, iter_index=1, star_wrap=0),  # https://github.com/BebeSparkelSparkel/functional_pipes/issues/3
    dict(gener=filter, name='filter_kargs', iter_index=1, double_star_wrap=0),  # https://github.com/BebeSparkelSparkel/functional_pipes/issues/3
    dict(gener=zip),
  )


map_methods_to_add = (
    dict(func=dict, name='dict_e'),
    dict(func=frozenset, name='frozenset_e'),
    dict(func=set, name='set_e'),
    dict(func=list, name='list_e'),
    dict(func=tuple, name='tuple_e'),
    dict(func=reversed, name='reversed_e'),

    dict(func=sorted, name='sorted_e'), # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    dict(func=max, name='max_e'), # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    dict(func=min, name='min_e'), # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4
    dict(func=sum, name='sum_e'), # https://github.com/BebeSparkelSparkel/functional_pipes/issues/4

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
