'''
custom testing tools that help debug your pipes
'''

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
