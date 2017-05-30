from itertools import count

from pipe import Pipe, Reservoir


class ResHandle:
  '''
  Handle to a thread of a Confluence instance.
  '''
  def __init__(self, res_id, confluence):
    self.res_id = res_id
    self.confluence = confluence

  def __call__(self, iterable):
    self.confluence.fill_res(iterable, self.res_id)

  def __iter__(self):
    return self

  def __next__(self):
    return self.confluence.next(self.res_id)


class Confluence:
  '''
  Multi threaded iterator that gives multiple handles to the beginning
  of the function pipe.
  '''

  get_id = iter(count())

  def __init__(self):
    self.reservoirs = {}

  def next(self, res_id):
    return next(self.reservoirs[res_id])

  def new_handle(self, iterable=None):
    res_id = next(self.get_id)
    self.reservoirs[res_id] = ReservoirMulti(iterable)

    return ResHandle(res_id, self)

  def fill_res(self, iterable, res_id):
    self.reservoirs[res_id](iterable)
