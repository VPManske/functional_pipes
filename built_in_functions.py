import pipe

output_container = (
    # collection

    # non iterable valves
    dict(gener=all, is_valve=True),
    dict(gener=any, is_valve=True),
    dict(gener=max, is_valve=True, empty_error=ValueError),

    # non valve functions
    dict(gener=enumerate),
    dict(gener=filter, iter_index=1, star_wrap=0),  # https://github.com/BebeSparkelSparkel/functional_pipes/issues/3
    dict(gener=filter, gener_name='filter_kargs', iter_index=1, double_star_wrap=0),  # https://github.com/BebeSparkelSparkel/functional_pipes/issues/3
    dict(gener=map, iter_index=1, star_wrap=0),
    dict(gener=map, gener_name='map_kargs', iter_index=1, double_star_wrap=0),
    dict(gener=zip)
  )

# gener,
# is_valve = False,
# iter_index = 0,
# gener_name = None,
# no_over_write = True,
# empty_error = None,
# star_wrap = None,
# double_star_wrap = None,

for method_properties in output_container:
  pipe.Pipe.add_method(**method_properties)