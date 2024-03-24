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
    assert len(empty_bit_array._arr) == 2  # 10 bits requires 2 bytes


def test_bad_init():
    with pytest.raises(TypeError):
        BitArray(5.5)

    with pytest.raises(TypeError):
        BitArray("hello")

    with pytest.raises(ValueError):
        BitArray(0)

    with pytest.raises(ValueError):
        BitArray(-5)


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


def test_or(filled_bit_array: BitArray, empty_bit_array: BitArray):
    empty_bit_array.bitwise_or(filled_bit_array)
    assert empty_bit_array.get(2) == 1
    assert empty_bit_array.get(5) == 1
    assert empty_bit_array.get(0) == 0


def test_prohibited_or(filled_bit_array: BitArray):
    arr = BitArray(3)
    with pytest.raises(ValueError):
        arr.bitwise_or(filled_bit_array)

    with pytest.raises(ValueError):
        arr.bitwise_or([0, 1, 0])


def test_memory():
    # For large sizes, will be much smaller than a list
    for i in range(500_000, 1_000_001, 100_000):
        lst = [0] * i
        b = BitArray(i)
        assert b.__sizeof__() < lst.__sizeof__() / 60


def test_iter():
    b = BitArray(3)
    for bit in b:
        assert bit == 0


def test_no_slices(filled_bit_array: BitArray):
    with pytest.raises(ValueError):
        filled_bit_array[0:]


def test_length(filled_bit_array: BitArray):
    assert len(filled_bit_array) == 10


def test_many_modifications():
    bit_array = BitArray(1000)
    for i in range(len(bit_array)):
        bit_array.set(i)
        assert bit_array.get(i) == 1

    for i in range(len(bit_array)):
        bit_array.clear(i)
        assert bit_array.get(i) == 0


def test_big_or():
    SIZE = 20_000
    bit_array_even = BitArray(SIZE)
    bit_array_odd = BitArray(SIZE)
    for i in range(0, SIZE - 1, 2):
        bit_array_even.set(i)

    for i in range(1, SIZE, 2):
        bit_array_odd.set(i)

    bit_array_odd.bitwise_or(bit_array_even)

    for i in range(SIZE):
        assert bit_array_odd.get(i) == 1
