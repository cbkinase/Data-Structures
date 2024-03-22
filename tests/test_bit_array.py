import pytest
from src import BitArray


@pytest.fixture
def empty_bit_array():
    return BitArray(10)


@pytest.fixture
def filled_bit_array():
    bit_array = BitArray(10)
    bit_array.set(2)
    bit_array.set(5)
    return bit_array


def test_initialization(empty_bit_array: BitArray):
    assert len(empty_bit_array.arr) == 2  # 10 bits requires 2 bytes


def test_setting_and_getting(empty_bit_array: BitArray):
    empty_bit_array.set(0)
    empty_bit_array.set(3)
    assert empty_bit_array.get(0) == 1
    assert empty_bit_array.get(1) == 0
    assert empty_bit_array.get(3) == 1


def test_clearing(empty_bit_array: BitArray):
    empty_bit_array.set(0)
    empty_bit_array.set(3)
    empty_bit_array.clear(0)
    assert empty_bit_array.get(0) == 0
    empty_bit_array.clear(3)
    assert empty_bit_array.get(3) == 0


def test_setting_and_getting_filled(filled_bit_array: BitArray):
    assert filled_bit_array.get(2) == 1
    assert filled_bit_array.get(5) == 1
    assert filled_bit_array.get(0) == 0


def test_set_and_clear(filled_bit_array: BitArray):
    filled_bit_array.clear(2)
    filled_bit_array.clear(5)
    assert filled_bit_array.get(2) == 0
    assert filled_bit_array.get(5) == 0
    assert filled_bit_array.get(0) == 0


def test_out_of_range(empty_bit_array: BitArray):
    with pytest.raises(IndexError):
        empty_bit_array.set(15)
    with pytest.raises(IndexError):
        empty_bit_array.clear(15)
    with pytest.raises(IndexError):
        empty_bit_array.get(15)


def test_xor(filled_bit_array: BitArray, empty_bit_array: BitArray):
    empty_bit_array.xor(filled_bit_array)
    assert empty_bit_array.get(2) == 1
    assert empty_bit_array.get(5) == 1
    assert empty_bit_array.get(0) == 0


def test_prohibited_xor(filled_bit_array: BitArray):
    arr = BitArray(3)
    with pytest.raises(ValueError):
        arr.xor(filled_bit_array)

    with pytest.raises(ValueError):
        arr.xor([0, 1, 0])


def test_memory():
    # For large sizes, will be much smaller than a list
    for i in range(100_000, 1_000_001, 100_000):
        lst = [0] * i
        b = BitArray(i)
        assert b.__sizeof__() < lst.__sizeof__() / 63


def test_big():
    BIG_NUM = 100_000_001
    big = BitArray(BIG_NUM)
    big_list = [0] * BIG_NUM
    assert len(big) == BIG_NUM
    # Some memory penalty with the generator for some reason... why?
    # Still, it remains true that space reduction approaches 64x, though
    # not monotonically anymore -- there is a jump at the size cutoff.
    assert big.__sizeof__() < big_list.__sizeof__() / 61


def test_iter():
    b = BitArray(3)
    for bit in b:
        assert bit == 0


def test_no_slices(filled_bit_array: BitArray):
    with pytest.raises(ValueError):
        filled_bit_array[0:]


def test_length(filled_bit_array: BitArray):
    assert len(filled_bit_array) == 10
