from functional_pipes.pipe import Pipe, Reservoir


class PipeMulti(Pipe):
  def __init__(self, function_pipe=None, reservoir=None, valve=False,
        iterable_pre_load=None  # placeholder for superclass pipe arguments
      ):
    self.preloaded = False

    # Iterable source for the Pipe
    self.reservoir = reservoir if reservoir else Confluence()

    # The chain of functions that data will be fed through.
    self.function_pipe = function_pipe if function_pipe else self.reservoir

    # True if the end of the pipe is a valve function else False
    self.valve = valve

  def __call__(self, iterable=None):
    return self.reservoir.new_handle(iterable)

  def __next__(self):
    return next(self.function_pipe)


class ResHandle:
  '''
  Handle to a thread of a Confluence instance.
  '''
  def __init__(self, confluence):
    self.confluence = confluence

  def __call__(self, iterable):
    self.confluence.fill_res(iterable, self)

  def __iter__(self):
    return self

  def __next__(self):
    return self.confluence.next(self)


class Confluence:
  '''
  Multi threaded iterator that gives multiple handles to the beginning
  of the function pipe.
  '''
  def __init__(self):
    self.reservoirs = {}

  def next(self, res_handle):
    return next(self.reservoirs[res_handle])

  def new_handle(self, iterable=None):
    res_handle = ResHandle(self)
    self.reservoirs[res_handle] = Reservoir(iterable)
    return res_handle

  def fill_res(self, iterable, res_handle):
    self.reservoirs[res_handle](iterable)
