from pipe import Reservoir

data = 1,2,3,4
refillable = Reservoir(data)

def super_gener(function):
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
        self.zipped = function(self.iterable)
        return next(self)

      except StopIteration as err:
        self.zipped = None
        raise err

  return wrapper_class


def hi(iterable):
  for val in iterable:
    yield val


hi_iter = super_gener(hi)(refillable)

print(tuple(hi_iter))
refillable(data)
print(tuple(hi_iter))