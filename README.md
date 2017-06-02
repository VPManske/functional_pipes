# functional_pipes
Functional transformation pipelines.

## Install
```shell
pip install git+https://github.com/BebeSparkelSparkel/functional_pipes@master
```

## Example usage:
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


## Built In Functions
### Import
To import the built in functions methods run code below. This will add the methods defined in built_in_functions.py to the Pipe class.
```python
from functional_pipes import Pipe, built_in_functions
```

### Methods
These methods will apply to all the data piped to them (not a per data element method).  
Methods that don't end in _kargs will automatically wrap a passed in arguments to the function with the * operator that. Example in Example Usage with comment "# automatic unpacking arguments".  
If a method ends with _kargs it means the function passed into it has the ** (keyed arguments).  
Pipe.**dict**()  
Pipe.**frozenset**()  
Pipe.**set**()  
Pipe.**list**()  
Pipe.**tuple**()  
Pipe.**all**()  
Pipe.**any**()  
Pipe.**max**(key)  
Pipe.**min**(key)  
Pipe.**max_kargs**(key)  
Pipe.**min_kargs**(key)  
Pipe.**sum**()  
Pipe.**sorted**(iterable[, key][, reverse])  
Pipe.**sorted_kargs**(iterable[, key][, reverse])  
Pipe.**enumerate**(start=0)  
Pipe.**filter**(function)  
Pipe.**filter_kargs**(function)  
Pipe.**map**(function)  
Pipe.**map_kargs**(function)  
Pipe.**zip**(*iterables)  
zips in the iterables with the piped data  

### Map Methods
Map Methods apply these methods to every element in the pipe.  
Right now they don't accept any arguments (work in progress). If you need to pass them an argument use the map method above.  
Pipe.**dict_e**()  
Pipe.**frozenset_e**()  
Pipe.**set_e**()  
Pipe.**list_e**()  
Pipe.**tuple_e**()  
Pipe.**reversed_e**()  
Pipe.**sorted_e**()  
Pipe.**max_e**()  
Pipe.**min_e**()  
Pipe.**sum_e**()  
Pipe.**str**()  
Pipe.**abs**()  
Pipe.**ascii**()  
Pipe.**bin**()  
Pipe.**bool**()  
Pipe.**callable**()  
Pipe.**chr**()  
Pipe.**classmethod**()  
Pipe.**staticmethod**()  
Pipe.**eval**()  
Pipe.**float**()  
Pipe.**hash**()  
Pipe.**hex**()  
Pipe.**id**()  
Pipe.**int**()  
Pipe.**iter**()  
Pipe.**len**()  
Pipe.**oct**()  
Pipe.**open**()  
Pipe.**ord**()  
Pipe.**range**()  
Pipe.**repr**()  
Pipe.**round**()  
Pipe.**type**()  

### Keyed Map Methods
Keyed Map Methods apply these methods to every element in the pipe and put it in a tuple (origional object, transformed object).  
Right now they don't accept any arguments (work in progress). If you need to pass them an argument use the map method above.  
Pipe.**dict_e_keyed**()  
Pipe.**frozenset_e_keyed**()  
Pipe.**set_e_keyed**()  
Pipe.**list_e_keyed**()  
Pipe.**tuple_e_keyed**()  
Pipe.**reversed_e_keyed**()  
Pipe.**sorted_e_keyed**()  
Pipe.**max_e_keyed**()  
Pipe.**min_e_keyed**()  
Pipe.**sum_e_keyed**()  
Pipe.**str_keyed**()  
Pipe.**abs_keyed**()  
Pipe.**ascii_keyed**()  
Pipe.**bin_keyed**()  
Pipe.**bool_keyed**()  
Pipe.**callable_keyed**()  
Pipe.**chr_keyed**()  
Pipe.**classmethod_keyed**()  
Pipe.**staticmethod_keyed**()  
Pipe.**eval_keyed**()  
Pipe.**float_keyed**()  
Pipe.**hash_keyed**()  
Pipe.**hex_keyed**()  
Pipe.**id_keyed**()  
Pipe.**int_keyed**()  
Pipe.**iter_keyed**()  
Pipe.**len_keyed**()  
Pipe.**oct_keyed**()  
Pipe.**open_keyed**()  
Pipe.**ord_keyed**()  
Pipe.**range_keyed**()  
Pipe.**repr_keyed**()  
Pipe.**round_keyed**()  
Pipe.**type_keyed**()  

## Custom Pipes
### Import
To import the built in functions methods run code below. This will add the methods defined in built_in_functions.py to the Pipe class.  
```python
from functional_pipes import Pipe, custom_pipes
```

Pipe.**zip_internal**()  
Zips all objects from iterable together.  

Example:  
```python
>>> data_1 = (1, 2, 3), (4, 5, 6), (7, 8, 9)
>>> Pipe(data_1).zip_internal().tuple()
((1, 4, 7), (2, 5, 8), (3, 6, 9))
```

Pipe.**dict_zip**()  
Yields a dictionary with the same keys that dict_w_iter has.  
The values are all of the same index from the iterator from the values from dict_w_iter.  

Example:  
```python
>>> data_dict = dict(
...    a = (1,2,3),
...    b = (4,5,6),
...  )
...
>>> for row in dict_zip(data_dict):
...  print(row)
...
{'a': 1, 'b': 4}
{'a': 2, 'b': 5}
{'a': 3, 'b': 6}
```

