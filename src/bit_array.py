"""
Time constraints on key permitted operations:

Let n be the size of the BitArray
and let i be the index an operation is performed on

   Operation    |     Time complexity   |      Notes
------------------------------------------------------------------------------
build(n)        |   -->     O(n)        |
clear_at(i)     |   -->     O(1)        |
get_at(i)       |   -->     O(1)        |
set_at(i)       |   -->     O(1)        |
or(other)       |   -->     O(n)        |
------------------------------------------------------------------------------

Overall, requires O(n) space. Practically, far less than a list for large n.
Asymptotically approaches a 64x reduction in space

Size of list/array   |   BitArray memory  |  List memory  |  Factor improved
------------------------------------------------------------------------------
10                   |      110 bytes     |   136 bytes   |    1.23x
1_000                |      233 bytes     |  8056 bytes   |   34.57x
100_000              |       12.50 KB     |   800.06 KB   |   63.46x
10_000_000           |        1.25 MB     |    80.00 MB   |   63.99x
100_000_000          |       12.50 MB     |   800.00 MB   |   64.00x
------------------------------------------------------------------------------
"""


import sys
from array import array
from itertools import repeat


class BitArray:
    def __init__(self, size: int):
        if not isinstance(size, int):
            raise TypeError("size must be an integer")

        if size <= 0:
            raise ValueError("size must be positive")

        self._size = size
        # It's a bit slower, but at a certain point the heap blows up...
        if size > 100_000_000:
            self._arr = array("B", repeat(0, (size + 7) // 8))
        else:
            self._arr = array("B", [0] * ((size + 7) // 8))

    def _check_index(self, index: int):
        """
        Ensure that index is within bounds of the array.

        No negative indices for now.
        """
        if index < 0 or index >= self._size:
            raise IndexError("Index out of range")

    def bitwise_or(self, other: "BitArray") -> None:
        """
        OR the bits of self with other, mutating self.

        BitArrays must be of equal length.
        """
        if not isinstance(other, BitArray):
            raise ValueError("Must OR with another BitArray")

        if self._size != other._size:
            raise ValueError("BitArrays must be of the same size")

        for i in range(len(self._arr)):
            self._arr[i] |= other._arr[i]

    def clear(self, index: int) -> None:
        """
        Set bit at index to 0.
        """
        self._check_index(index)
        self._arr[index // 8] &= ~(1 << (index % 8))

    def get(self, index: int) -> int:
        """
        Returns bit at index.
        """
        self._check_index(index)
        return (self._arr[index // 8] >> (index % 8)) & 1

    def set(self, index: int) -> None:
        """
        Set bit at index to 1.
        """
        self._check_index(index)
        self._arr[index // 8] |= 1 << (index % 8)

    def __getitem__(self, __index: int) -> int:
        if isinstance(__index, slice):
            raise ValueError("BitArray does not support slicing")

        return self.get(__index)

    def __len__(self) -> int:
        return self._size

    def __sizeof__(self) -> int:
        return sys.getsizeof(self._arr) + sys.getsizeof(self._size)
