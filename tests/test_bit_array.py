import pytest
from src import BitArray


@pytest.fixture
def empty_bit_array():
    return BitArray(10)


@pytest.fixture
def filled_bit_array():
    bit_array = BitArray(10)
    bit_array[2] = 1
    bit_array[5] = 1
    return bit_array


def test_bad_init():
    with pytest.raises(TypeError):
        BitArray(5.5)

    with pytest.raises(TypeError):
        BitArray("hello")

    with pytest.raises(ValueError):
        BitArray(0)

    with pytest.raises(ValueError):
        BitArray(-5)


def test_setitem(empty_bit_array: BitArray):
    empty_bit_array[0] = 1
    assert empty_bit_array[0] == 1
    empty_bit_array[0] = 0
    assert empty_bit_array[0] == 0


def test_getitem(filled_bit_array: BitArray):
    assert filled_bit_array[2] == 1
    assert filled_bit_array[5] == 1
    assert filled_bit_array[0] == 0


def test_iter(empty_bit_array: BitArray):
    for bit in empty_bit_array:
        assert bit == 0


def test_length(filled_bit_array: BitArray):
    assert len(filled_bit_array) == 10


def test_many_modifications():
    bit_array = BitArray(1000)
    for i in range(len(bit_array)):
        bit_array[i] = 1
        assert bit_array[i] == 1

    for i in range(len(bit_array)):
        bit_array[i] = 0
        assert bit_array[i] == 0


def test_or():
    SIZE = 20_000
    bit_array_even = BitArray(SIZE)
    bit_array_odd = BitArray(SIZE)
    for i in range(0, SIZE - 1, 2):
        bit_array_even[i] = 1

    for i in range(1, SIZE, 2):
        bit_array_odd[i] = 1

    bit_array_odd.bitwise_or(bit_array_even)

    for i in range(SIZE):
        assert bit_array_odd[i] == 1


def test_prohibited_or():
    arr = BitArray(3)

    with pytest.raises(ValueError):
        arr.bitwise_or(BitArray(5))

    with pytest.raises(TypeError):
        arr.bitwise_or([0, 1, 0])


def test_memory():
    # For large sizes, BitArray will be much smaller than a list
    for i in range(1_000_000, 2_000_001, 100_000):
        lst = [0] * i
        b = BitArray(i)
        assert pytest.approx(b.__sizeof__(), rel=0.01) == lst.__sizeof__() / 60
