'''
Use to carry values around multiple pipe segments
and reconnect them later.
'''


class Bypass:
  '''
  Use to carry values around a pipe segment and reconnect them.

  The self.store object will be merged the object that is put through the bypass.

  If the bypass iterator creates more values than is put into it the self.store
  object that caome from split will be given to each of the values.

  If the bypass iterator does not return a value for the input then the self.store
  object is dropped and the next object from iterable is put into the bypass.
  '''
  def __init__(self, bypass, iterable, drip_handle, split, merge):
    '''
    bypass - Inteded to be a Pipe but it can be any iterator that initally iterates
      over drip_handle.
    iterable - Intended to be a Pipe but it can be any iterator that's output will
      be run through split.
    drip_handle - Needs to be an instance of the Drip class that is the root
      iterator of the bypass argument.
    split - function that returns a tuple that splits the object from the
      iterable argument and returns a tuple of length two. The zero index will be
      the value that is carried around the bypass and passed into the merge
      function as the first argument. The one index will be passed into the bypass
      to be modified.
    merge - function that takes in two arguments and returns a single object.
      The first argument comes from the zero index output from split and the
      second argument is the value returned from the bypass.
    '''
    self.bypass = bypass
    self.iterable = iter(iterable)
    self.drip_handle = drip_handle
    self.split = split
    self.merge = merge

    self.store = None

  def __next__(self):
    try:
      to_return = self.merge(self.store, next(self.bypass))

    except Drip:
      for next_obj in self.iterable:
        self.store, pass_on = self.split(next_obj)
        self.drip_handle(pass_on)

        try:
          to_return = self.merge(self.store, next(self.bypass))
          break
        except Drip:
          continue

      else:
        raise StopIteration

    return to_return

  def __iter__(self):
    return self


class Drip(Exception):
  '''
  An iterator that only allows one object out at a time before throwing an exception.
  Initially empty.
  Call with an object to return when next is called on it.
  After first next is called the second next will raise a Drip exception.
  Used by the Bypass class to control flow into the bypass pipe.
  '''
  def __init__(self):
    self.to_drip = _drip_empty

  def __call__(self, next_drip):
    '''
    Sets the next vale to be returned by next.
    '''
    self.to_drip = next_drip

  def __next__(self):
    '''
    Returns value passed in by call once and then raises Drip excpetion.
    '''
    if self.to_drip is not _drip_empty:
      to_return = self.to_drip
      self.to_drip = _drip_empty
      return to_return

    raise Drip

  def __iter__(self):
    return self

class _drip_empty:
  '''
  Exclusive use in Drip class for indicating if it is empty or not.
  '''
  pass


def close_bypass_default(close_name):
  '''
  courier function for close_bypass

  close_name - name of the closing property

  Needs unit test
  '''
  def close_bypass(self):
    '''
    Closes the bypass that was opened with open_bypass.
    Checks to make sure open_bypass and close_bypass matches.
    '''
    enclosing_pipe = self.enclosing_pipe
    b_props = self.bypass_properties

    if b_props.close_name != close_name:
      '''
      Checks that opening and closing operators match.
      '''
      raise TypeError('Recieved a {} but was expecting a {} when closing a {} bypass Pipe.'.format(
          close_name, b_props.close_name, b_props.open_name,))

    bpp = Bypass(
        bypass = self,
        iterable = enclosing_pipe,
        drip_handle = self.reservoir,
        split = b_props.split,
        merge = b_props.merge,
      )

    pipe_class = self.enclosing_pipe.__class__

    return pipe_class(
        iterable_pre_load = enclosing_pipe.preloaded,
        function_pipe = bpp,
        reservoir = enclosing_pipe.reservoir,
      )

  return close_bypass
