'''
Cannot be used yet.
'''

import more_itertools as mi


# gener,
# is_valve = False,
# iter_index = 0,
# name = None,
# no_over_write = True,
# empty_error = None,
# star_wrap = None,
# double_star_wrap = None,
methods_to_add = (
  # iterable valves
  dict(gener=mi.chunked, is_valve=True),
  dict(gener=mi.distribute, is_valve=True, iter_index=1),
  dict(gener=mi.divide, is_valve=True, iter_index=1),

  # non valve
  dict(gener=mi.split_before, star_wrap=1),
  dict(gener=mi.split_before, name='split_before_kargs',  double_star_wrap='pred'),
  dict(gener=mi.split_after, star_wrap=1),
  dict(gener=mi.split_after, name='split_after_kargs',  double_star_wrap='pred'),

)
maps_to_add = (

)
not_added = (
mi.sliced
)