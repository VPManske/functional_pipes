class dotdict(dict):
  '''
  dictionary that works with dot notation
  http://stackoverflow.com/questions/2352181/how-to-use-a-dot-to-access-members-of-dictionary
  '''
  __getattr__ = dict.get
  __setattr__ = dict.__setitem__
  __delattr__ = dict.__delitem__