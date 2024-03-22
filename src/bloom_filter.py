"""
Time constraints on key permitted operations:

Let m be the size of the bit array
Let n be the number of inserted elements (sometimes called expected insertions)
Let k be the number of hash functions

   Operation         |     Time complexity   |      Notes
------------------------------------------------------------------------------
expected_fpp()       |   -->     O(1)        |  Probability of false positive*
is_compatible(other) |   -->     O(1)        |
might_contain(item)  |   -->     O(k)        |  Potentially false positive
put(item)            |   -->     O(k)        |
------------------------------------------------------------------------------

Optimal number for m:
m = ceil((n * log(p)) / log(1 / pow(2, log(2))))
where p is the desired false positive probability

Optimal number for k:
k = round((m / n) * log(2))

------------------------------------------------------------------------------
    * Notes on the probability of false positives:
------------------------------------------------------------------------------
- Intuitively: depends on the density of 1's in the bit array and k
    - = (fraction of 1's) ** k
- Density of 1's: proportional to k * n
    - Slightly lower due to collisions
    - Probability that nothing hashes to a certain index:
        - (1 - 1 / m) ** (k * n) <==> (1 - 1 / m) ** (m * (k * n) / m)
        - lim as m->infinity: (1 - 1/m) ** m = e
        - Thus, approximate as e ** - ((k * n) / m)
- Ex: m = 1 billion, k = 5, n = 100 million
    - Fraction of 0's = 1 / (e ** (k * n) / m)
    - = e ** -(1/2) = 0.607
    - Fraction of 1's = 1 - 0.607 = 0.393
    - P(false positive) = 0.393 ** 5 = 0.00937

Side note:
TDD with probabilistic data structures... how does it work? Monte Carlo?
"""


import hashlib
from math import ceil
from math import exp
from math import log
from math import pow
from typing import Hashable
from src.bit_array import BitArray


class BloomFilter:
    _hash_fn_names = list(hashlib.algorithms_guaranteed)
    _hash_fn_names = [
        name for name in _hash_fn_names if not name.startswith("shake")
    ]

    def __init__(self, expected_insertions: int, fp_rate: float = 0.03):
        self._expected_insertions = expected_insertions
        self._fp_rate = fp_rate
        self._bit_array: BitArray = self._initialize_bit_array()
        self._hash_functions = self._pick_hash_functions()

    def _initialize_bit_array(self):
        n = self._expected_insertions
        p = self._fp_rate
        length = ceil((n * log(p)) / log(1 / pow(2, log(2))))
        return BitArray(length)

    def _pick_hash_functions(self):
        n = self._expected_insertions
        m = len(self._bit_array)
        k = round((m / n) * log(2))
        # Pick first k hash functions
        return [hashlib.new(name) for name in BloomFilter._hash_fn_names[:k]]

    def expected_fpp(self) -> float:
        """
        Returns the probability that might_contain(item) will erroneously
        return true for an item that has not actually been put in the
        BloomFilter.
        """
        k = len(self._hash_functions)
        n = self._expected_insertions
        m = len(self._bit_array)
        expected_zero_density = exp(-(k * n) / m)
        return (1 - expected_zero_density) ** k

    def is_compatible(self, other) -> bool:
        # For two BloomFilters to be compatible, they...

        if not isinstance(other, BloomFilter):
            # Must be a BloomFilter
            return False

        if id(self) == id(other):
            # Must not be the same instance
            return False

        if len(self._hash_functions) != len(other._hash_functions):
            # Must have the same number of hash functions
            return False

        if len(self._bit_array) != len(other._bit_array):
            # Must have the same bit array size
            return False

        return True

    def may_contain(self, item: Hashable) -> bool:
        """
        Returns true if the item might have been put in this BloomFilter,
        false if this is definitely not the case.
        """
        for hasher in self._hash_functions:
            hasher = hasher.copy()
            hasher.update(str(item).encode())
            digest = hasher.digest()
            hash_int = int.from_bytes(digest, byteorder="big")
            bucket = hash_int % len(self._bit_array)

            if self._bit_array.get(bucket) == 0:
                return False

        return True

    def put(self, item: Hashable) -> None:
        """Put an element into the BloomFilter"""
        for hasher in self._hash_functions:
            hasher = hasher.copy()
            hasher.update(str(item).encode())
            digest = hasher.digest()
            hash_int = int.from_bytes(digest, byteorder="big")
            bucket = hash_int % len(self._bit_array)
            self._bit_array.set(bucket)

    def put_all(self, other) -> None:
        """
        Combines this BloomFilter with another BloomFilter by performing
        a bitwise OR of the underlying bit arrays.
        """
        if self.is_compatible(other):
            self._bit_array.xor(other._bit_array)
        else:
            raise ValueError("Bloom filters are not compatible")

    def __contains__(self, item) -> bool:
        """Included for uniformity with other container types"""
        return self.may_contain(item)
