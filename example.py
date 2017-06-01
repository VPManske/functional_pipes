from functional_pipes import Pipe, built_in_functions

data_1 = 1, -2, 3, -4, 5

# single use pipe
print(
  Pipe(data_1).abs().range().tuple_e().tuple()
)

print(
  Pipe(data_1).abs().max()
)

data_2 = (1, 2), (3, 4), (5, 6)
data_3 = (4, 2), (5, 9), (1, 7), (2, 5)

# reuse pipe
reuse = Pipe(
  ).map(lambda a, b: (2 * a, b, a * b)
  ).filter(lambda a2, b, ab: a2 < ab and a2 < b  # automatic unpacking arguments
  ).list()  # convert to any built in collection

print(
  reuse(data_2)
)
print(
  reuse(data_3)
)

# extend existing pipes
extended = reuse.min_e(  # min by element
  ).tuple()  # put into tuple

print(
  extended(data_3)
)

