def wrap_gener(generator):
  '''
  Used to wrap generators so that they can be reused.

  generator - any generator that cannot be reused once StopIteration is thrown
  '''
  class wrapper_class:
    def __init__(self, iterable):
      self.iterable = iterable
      self.gener_iter = None

    def __iter__(self):
      return self

    def __next__(self):
      try:
        return next(self.gener_iter)

      except TypeError:
        # reload the generator and return the next value
        self.gener_iter = generator(self.iterable)
        return next(self)

      except StopIteration as err:
        # empty gener_iter and then let StopIteration propigate
        self.gener_iter = None
        raise err

  # sets the wrapper to have the same name as the generator it is wrapping
  wrapper_class.__name__ = generator.__name__

  return wrapper_class


