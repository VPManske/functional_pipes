class hi:
  def __init__(self, above):
    self.above = above

  def __getitem__(self, index):
    return 'get' + index

class there:
  pass


setattr(there, 'hi', property(hi))

buddy = there()
print(buddy.hi['6'])