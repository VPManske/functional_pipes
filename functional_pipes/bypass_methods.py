'''
Bypass method definitions
'''

from functional_pipes.more_collections import dotdict
from functional_pipes.bypass import Drip, close_bypass_default


def add_bypasses(pipe_class):
  for definition in bypass_definitions:
    pipe_class.add_bypass(**definition)



class dict_carry_open:
  '''
  Class that allows dictionary object to bypass a Pipe.
  '''
  open_name = 'carry_dict'
  close_name = 'return_dict'

  def __init__(self, enclosing_pipe):
    self.enclosing_pipe = enclosing_pipe

  def __getitem__(self, key):
    '''
    self - pipe instance
    '''
    enclosing_pipe = self.enclosing_pipe

    def merge(dictionary, value):
      dictionary[key] = value
      return dictionary

    pipe_class = self.enclosing_pipe.__class__

    return pipe_class(
        reservoir = Drip(),
        enclosing_pipe = enclosing_pipe,
        bypass_properties = dotdict(
            open_name = self.open_name,
            close_name = self.close_name,
            split = lambda dictionary: (dictionary, dictionary[key]),
            merge = merge,
          ),
      )


class dict_key:
  '''
  allows the dict to bypass one pipe segment
  '''
  open_name = 'dict_key'

  def __init__(self, enclosing_pipe):
    self.enclosing_pipe = enclosing_pipe

  def __getitem__(self, key):
    '''
    self - pipe instance
    '''
    enclosing_pipe = self.enclosing_pipe

    def merge(dictionary, value):
      dictionary[key] = value
      return dictionary

    pipe_class = self.enclosing_pipe.__class__

    return pipe_class(
        reservoir = Drip(),
        enclosing_pipe = enclosing_pipe,
        bypass_properties = dotdict(
            open_name = self.open_name,
            close_name = None,
            split = lambda dictionary: (dictionary, dictionary[key]),
            merge = merge,
            close_bypass = close_bypass_default(None),
          ),
      )


bypass_definitions = (
    dict(
        open_name = 'carry_key',
        close_name = 're_key',
        split = lambda key_val: (key_val[0], key_val[1]),
        merge = lambda key, bypass_val: (key, bypass_val),
      ),
    dict(
        open_name = 'keyed',
        split = lambda value: (value, value),
        merge = lambda key, bypass_val: (key, bypass_val),
      ),
    dict(
        open_name = 'carry_value',
        close_name = 're_value',
        split = lambda key_val: (key_val[1], key_val[0]),
        merge = lambda val, bypass_key: (bypass_key, val),
      ),
    dict(
        open_name = dict_carry_open.open_name,
        close_name = dict_carry_open.close_name,
        open_bypass = property(dict_carry_open),
      ),
    dict(
        open_name = dict_key.open_name,
        open_bypass = property(dict_key),
      ),
  )
