def wrap_gener(generator):
  class wrapper_class:
    def __init__(self, iterable):
      self.iterable = iterable
      self.zipped = None

    def __iter__(self):
      return self

    def __next__(self):
      try:
        return next(self.zipped)

      except TypeError:
        self.zipped = generator(self.iterable)
        return next(self)

      except StopIteration as err:
        self.zipped = None
        raise err

  wrapper_class.__name__ = generator.__name__

  return wrapper_class


