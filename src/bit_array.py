"""
Time constraints on key permitted operations:

Let n be the size of the BitArray
and let i be the index an operation is performed on

   Operation    |     Time complexity   |      Notes
------------------------------------------------------------------------------
build(n)        |   -->     O(n)        |
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
Numbers may vary slightly depending on the Python implementation, version, etc
"""


import sys
from array import array


class BitArray:
    def __init__(self, size: int):
        if not isinstance(size, int):
            raise TypeError("size must be an integer")

        if size <= 0:
            raise ValueError("size must be positive")

        self._size = size
        # Each slot in self._arr holds 8 bits
        self._arr = array("B", bytearray((size + 7) // 8))

    def bitwise_or(self, other: "BitArray") -> None:
        """
        OR the bits of self with other, mutating self.

        BitArrays must be of equal length.
        """
        if not isinstance(other, BitArray):
            raise TypeError("Must OR with another BitArray")

        if self._size != other._size:
            raise ValueError("BitArrays must be of the same size")

        for i in range(len(self._arr)):
            self._arr[i] |= other._arr[i]

    def __getitem__(self, __key: int) -> int:
        return (self._arr[__key // 8] >> (__key % 8)) & 1

    def __setitem__(self, __key: int, __value: int) -> None:
        if __value == 1:
            self._arr[__key // 8] |= 1 << (__key % 8)
        elif __value == 0:
            self._arr[__key // 8] &= ~(1 << (__key % 8))

    def __len__(self) -> int:
        return self._size

    def __sizeof__(self) -> int:
        return sys.getsizeof(self._arr) + sys.getsizeof(self._size)
