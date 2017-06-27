'''
Methods from numpy

Will probably have to be expanded into multiple libries.
'''

import numpy as np


method_names = set() # holds all the method names that were added to Pipe


methods_to_add = (
    dict(gener=np.fromiter, is_valve=True),
  )


map_methods_to_add = ()
