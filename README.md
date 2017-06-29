# functional_pipes
Functional transformation pipelines.  
✮✮✮✮✮✮✮✮✮✮✮✮ LIKE IT? STAR IT! ✮✮✮✮✮✮✮✮✮✮✮✮  
![](https://github.com/BebeSparkelSparkel/functional_pipes/blob/master/water-pipes-flowing1.jpg?raw=true)

## Install
```shell
pip install git+https://github.com/BebeSparkelSparkel/functional_pipes@master
```
Will add to pypi if people show interest in this.  

## Example usage:

### Simple
Very simple example of a map reduce.  
This apples the absolute value to each of the numbers and then reduces to the maximum value.  
```python
data = 1, -2, -3
absolute_max = Pipe(data).abs().max()

print(absolute_max)
```

### Reusable Piping
A pipe can be created without any data preloaded and be run multiple times without being rebuilt each time. This is useful because it means you can put the prebuilt pipe into a loop without the overhead of rebuilding it for every iteration.  

One system that this is good for is outline below:  
  1.) generates data  
  2.) runs the data through the pipe  
  3.) makes changes to the data based on the result from the pipe  
  4.) rerun the changed data through the pipe  
  5.) repeat steps  

The example below shows an implimentation of this system:  
```python
data = (20, 2), (50, 9), (100, 7), (2, 5)

reusable_pipe = Pipe(
  ).map(lambda a, b: (20 * a, a * b)  # notice how the tuple is split automatically
  ).filter(lambda ax2, ab: ax2 > ab
  ).list()  # convert to a collection object

loop_count = 0
while len(data) >= 2 and loop_count < 5000:
  data = reusable_pipe(data)
  loop_count += 1

print(data)
```

### Extenable Pipes
Pipes can also be extended from a previous pipe and both pipes will still work.  
```python
data = 'hi', 'there', 'everyone'

first_letter = Pipe().map(lambda word: word[0].upper() + word[1:])

all_letters = first_letter.map(lambda word: word.upper()).tuple()

# Pipes can also be used like an iterator
for word in first_letter(data):
  print(word)

print(all_letters(data))
```

### Adding Methods (It is SOOOO EASY!)
So, you thought that the above lambda functions were ugly and hard to read. We can fix that with Pipe.add_method or Pipe.add_map_method. Those methods allow for simple and complex methods to be added to Pipe.  

Below is an example of how to add the above examples methods to Pipe and get the same result.  
```python
# this as the string class method upper
Pipe.add_map_method(str.upper)

# lambda functions can also be added
Pipe.add_map_method(
  lambda word: word[0].upper() + word[1:],
  name = 'first_upper'
)

# lets try again and see how much better this looks
first_letter = Pipe().first_upper()

all_letters = first_letter.upper().tuple()
```

### Carry Values
Meaning, avoiding the bs of passing values through every function and having to work around them in every method.  

This allows you to carry the key/value in a key value pair, a dict, list, or object that you create a method for arround a series of operations that only need to be applied to that value.  

The data can expand or shrink in this process and be ok. If the data shrinks the carry value is dropped. If the data expands the carry value will be applied to each of the expanded objects.  
```python
# (name, age)
data = ('John', 5), ('Billy', 9), ('Cait', 12), ('April', 2)

result = Pipe(data
  ).carry_key.add(1  # carry_key splits the key value pair and passes the age value to add
    ).filter(lambda age: age >= 10  # shrinks data size
  ).re_key.tuple()  # re_key is called the name and modified age are put back together

print(result)

# also works with dictionaries
data = (
  dict(name='John',  age=5),
  dict(name='Billy', age=9),
  dict(name='Cait',  age=12),
  dict(name='April', age=2),
)

result = Pipe(data
  ).carry_dict['age'].add(1  # carry_dict splits the dictionary and age value
    ).filter(lambda age: age >= 10  # shrinks data size
  ).return_dict.tuple()  # return_dict combines the dictionary and modified age

print(result)
```

## Built In Functions
### Import
To import the built in functions methods run code below. This will add the methods defined in built_in_functions.py to the Pipe class.  
```python
from functional_pipes import Pipe

# loads the add-in built_in_functions
Pipe.load('built_in_functions')
```

### Methods
These methods will apply to all the data piped to them (not a per data element method).  
Methods that don't end in _kargs will automatically wrap a passed in arguments to the function with the \* operator that. Example in Example Usage with comment "# automatic unpacking arguments".  
If a method ends with _kargs it means the function passed into it has the \*\* (keyed arguments).  
Pipe.**dict**()  
Should only be used for closing a Pipe because if another segement draws from dict the next segment will only get the keys and the the values.  
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
from functional_pipes import Pipe
Pipe('custom_pipes')
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

## About This Repo
I decided to write this package because I wanted to have more functional programming concepts in python.  
This is still a work in progress that I would like to continue to improve. If you have comments, suggestions, or bugs please create an issue.  

## Coming Soon
I would like to add the functionality from itertools and [more-itertools](https://github.com/erikrose/more-itertools) to this along with some custom functions that I think would be useful.

✮✮✮✮✮✮✮✮✮✮✮✮ LIKE IT? STAR IT! ✮✮✮✮✮✮✮✮✮✮✮✮  
