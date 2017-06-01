# functional_pipes
Functional transformation pipelines.

```python
>>> from functional_pipes import Pipe, built_in_functions
>>> 
>>> data_1 = 1, -2, 3, -4, 5
>>> 
>>> # single use pipe
... Pipe(data_1).abs().range().tuple_e().tuple()
((0,), (0, 1), (0, 1, 2), (0, 1, 2, 3), (0, 1, 2, 3, 4))
>>> 
>>> Pipe(data_1).abs().max()
5
>>> 
>>> data_2 = (1, 2), (3, 4), (5, 6)
>>> data_3 = (4, 2), (5, 9), (1, 7), (2, 5)
>>> 
>>> # reuse pipe
... reuse = Pipe(
...   ).map(lambda a, b: (2 * a, b, a * b)
...   ).filter(lambda a2, b, ab: a2 < ab and a2 < b  # automatic unpacking arguments
...   ).list()  # convert to any built in collection
>>> 
>>> reuse(data_2)
[]
>>> reuse(data_3)
[(2, 7, 7), (4, 5, 10)]
>>> 
>>> # extend existing pipes
... extended = reuse.min_e(  # min by element
...   ).tuple()  # put into tuple
>>> 
>>> extended(data_3)
(2, 4)
```