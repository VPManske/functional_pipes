from functional_pipes import Pipe
Pipe.load('built_in_functions', 'operator_pipes')

'''
Very simple example of a map reduce.
This apples the absolute value to each of the numbers and then reduces to the
maximum value.
'''
data = 1, -2, -3
absolute_max = Pipe(data).abs().max()

print(absolute_max)



'''
Reusable Piping
A pipe can be created without any data preloaded and be run multiple
times without being rebuilt each time. This is useful because it means you can put
the prebuilt pipe into a loop without the overhead of rebuilding it for every
iteration.

One system that this is good for is outline below:
  1.) generates data
  2.) runs the data through the pipe
  3.) makes changes to the data based on the result from the pipe
  4.) rerun the changed data through the pipe
  5.) repeat steps
The example below shows an implimentation of this system:
'''
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

'''
Extenable Pipes
Pipes can also be extended from a previous pipe and both pipes will still work.

Warning: Make sure you exhaust the iterable that is put into each the origional pipe
         or the extended pipe because they draw from the same source. Luckily an error
         is raised if you attempt this.
         If you want to draw from multiple sources with the same pipe simultaneously
         look at the class PipeMulti in pipe_multi.py.
  Example:
    >>> pipe_original = Pipe().do_something()
    >>> pipe_extended = pipe_original.do_more_somethings()
    >>>
    >>> pipe_original(data_1)
    >>> pipe_extended(data_2)  # this is bad because data_1 hasn't been used yet
'''
data = 'hi', 'there', 'everyone'

first_letter = Pipe().map(lambda word: word[0].upper() + word[1:])

all_letters = first_letter.map(lambda word: word.upper()).tuple()


# Pipes can also be used like an iterator
for word in first_letter(data):
  print(word)

print(all_letters(data))

'''
Adding Methods (It is SOOOO EASY!)
So, you thought that the above lambda functions were ugly and hard to read. We can
fix that with Pipe.add_method or Pipe.add_map_method. Those methods allow for simple
and complex methods to be added to Pipe.

Below is an example of how to add the above examples methods to Pipe and get the
same result.
'''

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


'''
Carry Values
Meaning, avoiding the bs of passing values through every function and having to work around
them in every method.

This allows you to carry the key/value in a key value pair, a dict, list, or object that you
create a method for arround a series of operations that only need to be applied to that value.

The data can expand or shrink in this process and be ok. If the data shrinks the carry value
is dropped. If the data expands the carry value will be applied to each of the expanded objects.
'''
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



