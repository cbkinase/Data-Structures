# About

This is an assortment of pure Python implementations of some miscellaneous data structures that I've either felt would be useful to have or just wanted to learn more about.

The data structures require no external dependencies: only core Python and the standard library are used.

## BitArray

<b> The BitArray data structure is highly space efficient, using only ~1.6% of the memory of an equal sized dynamic array for large array sizes -- 64 times less space. </b>


Let n be the size of the `BitArray`\
Let i be the index we are operating on

|   Operation  	| Time Complexity 	|                 Notes                	|
|:------------:	|:---------------:	|:------------------------------------:	|
|   build(n)   	|       O(n)      	|                                      	|
|   get_at(i)  	|       O(1)      	|          Return bit at index         	|
| set_at(i, b) 	|       O(1)      	|           Set bit at i to b          	|
|   or(other)  	|       O(n)      	| Bitwise OR two same-length BitArrays 	|


<sub>`bit_array.get_at(i)` is written as `bit_array[i]`</sub>\
<sub>`bit_array.set_at(i, b)` is written as `bit_array[i] = b`


## BloomFilter

<b> A probabilistic data structure supporting highly memory efficient membership testing, provided you are willing to accept a certain (predictable) level of inaccuracy. </b>


Let m be the size of the bit array\
Let n be the number of inserted elements (sometimes called expected insertions)\
Let k be the number of hash functions\
Let p be the probability of a false positive after n distinct insertions

|       Operation      |   Time Complexity  |             Notes             |
|:--------------------:|:------------------:|:-----------------------------:|
|      build(n, p)     | O(n * abs(log(p))) |           0 < p < 1           |
|    expected_fpp()    |        O(1)        | Probability of false positive |
| is_compatible(other) |        O(1)        |                               |
|  might_contain(item) |        O(k)        |   Potentially false positive  |
|       put(item)      |        O(k)        |                               |


## UniqueList

<b> May also be thought of as an `OrderedSet`. Essentially has the interface of a list that does not allow duplicate entries. Only hashable (immutable) types may be added to `UniqueList` -- otherwise it becomes impossible to guarantee uniqueness. </b>

Let n be the number of elements in the `UniqueList`\
Let i be the index we are operating on


|    Operation    	| Time Complexity 	|               Notes               	|
|:---------------:	|:---------------:	|:---------------------------------:	|
|   append(item)  	|       O(1)      	|           Amortized O(1)          	|
|  contains(item) 	|       O(1)      	|         Use underlying set        	|
|   delete_at(i)  	|       O(n)      	| Worst case (i=0), O(1) at i = n-1 	|
|    get_at(i)    	|       O(1)      	|                                   	|
| insert(i, item) 	|       O(n)      	|  Worst case (i=0), O(1) at i = n  	|
| set_at(i, item) 	|       O(1)      	|                                   	|
|   remove(item)  	|       O(n)      	|   Find i of item + delete_at(i)   	|


<sub>`unique_list.delete_at(i)` is written as `del unique_list[i]`</sub>\
<sub>`unique_list.get_at(i)` is written as `unique_list[i]`</sub>\
<sub>`unique_list.set_at(i, item)` is written as `unique_list[i] = item`. Throws ValueError if `item` is already in `UniqueList` instance.</sub>


## Development

- Install testing dependencies: `pip install -r requirements.txt`
- Testing: `pytest` or `pytest --cov=src` for coverage reports
- Formatting: `black .`
