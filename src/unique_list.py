"""
Time constraints on key permitted operations:

Let n be the number of elements in the UniqueList
and let i be the index

   Operation    |     Time complexity   |      Notes
------------------------------------------------------------------------------
append(item)    |   -->     O(1)        |   Amortized O(1)
contains(item)  |   -->     O(1)        |   Use underlying set
delete_at(i)    |   -->     O(n)        |   Worst case (i=0), O(1) at i = n-1
get_at(i)       |   -->     O(1)        |
insert(i, item) |   -->     O(1)        |   Worst case (i=0), O(1) at i = n
set_at(i)       |   -->     O(1)        |
remove(item)    |   -->     O(n)        |   Find i of item + delete_at(i)
------------------------------------------------------------------------------

Overall, requires O(n) space

Open question for now:
Is it possible to extend the data structure to allow non-hashable
entries while preserving the time complexity of these operations?
(I think not, but would be interested if someone can prove me wrong)

Is it better to call this structure a "UniqueList" or an "OrderedSet"?
"""


from collections.abc import MutableSequence
from typing import Any
from typing import Hashable
from typing import Iterable
from typing import SupportsIndex


class UniqueList(MutableSequence):
    """
    A mutable, ordered collection allowing only unique, hashable entries.
    """

    def __init__(self, iterable: Iterable = None):
        self._lst = []
        self._hsh = set()

        if iterable:
            self.extend(iterable)

    def append(self, item: Hashable, *, strict: bool = False) -> None:
        """
        Add item to the end of UniqueList.

        If `strict` is enabled, will throw a ValueError
        when duplicate entries are added. Does nothing otherwise.
        """
        if item not in self._hsh:
            self._lst.append(item)
            self._hsh.add(item)
        else:
            if strict:
                raise ValueError("Cannot insert duplicate entry")

    def clear(self) -> None:
        self._lst.clear()
        self._hsh.clear()

    def extend(self, iterable: Iterable, *, strict: bool = False) -> None:
        """
        Extend UniqueList by appending elements from the iterable.
        """
        for item in iterable:
            self.append(item, strict=strict)

    def insert(
        self, __index: SupportsIndex, item: Hashable, *, strict: bool = False
    ) -> None:
        """
        Insert item before index.

        If `strict` is enabled, will throw a ValueError
        when duplicate entries are added. Does nothing otherwise.
        """
        if item not in self._hsh:
            self._lst.insert(__index, item)
            self._hsh.add(item)
        else:
            if strict:
                raise ValueError("Cannot insert duplicate entry")

    def pop(self, __index: SupportsIndex = -1) -> Any:
        """
        Remove and return item at index (default last).

        Raises IndexError if UniqueList is empty or index is out of range.
        """
        item = self._lst.pop(__index)
        self._hsh.remove(item)
        return item

    def remove(self, item: Hashable) -> None:
        """
        Remove specified item from UniqueList.

        Raises ValueError if item is not present.
        """
        self._lst.remove(item)
        self._hsh.remove(item)

    def reverse(self) -> None:
        self._lst.reverse()

    def __bool__(self) -> bool:
        return bool(self._lst)

    def __contains__(self, item: Hashable) -> bool:
        return item in self._hsh

    def __delitem__(self, __key: SupportsIndex) -> None:
        """
        Delete self[key].
        """
        val = self._lst[__key]
        self._hsh.remove(val)
        del self._lst[__key]

    def __getitem__(self, __index: SupportsIndex):
        """
        x.__getitem__(y) <==> x[y]
        """
        # TODO: slice of UniqueList should return UniqueList, not list
        return self._lst[__index]

    def __len__(self) -> int:
        return len(self._lst)

    def __repr__(self) -> str:
        return f"UniqueList({str(self._lst)})"

    def __setitem__(self, __index: SupportsIndex, item: Hashable) -> None:
        if item in self._hsh:
            raise ValueError("Cannot insert duplicate entry")

        old_item = self._lst[__index]
        self._hsh.remove(old_item)
        self._lst[__index] = item
