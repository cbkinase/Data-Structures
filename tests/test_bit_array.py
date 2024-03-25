import pytest
from src import BitArray, BitArrayFast


@pytest.fixture(params=[BitArray, BitArrayFast])
def empty_bit_array(request):
    return request.param(10)


@pytest.fixture(params=[BitArray, BitArrayFast])
def filled_bit_array(request):
    bit_array_cls = request.param
    bit_array = bit_array_cls(10)
    bit_array[2] = 1
    bit_array[5] = 1
    return bit_array


@pytest.mark.parametrize("BitArrayClass", [BitArray, BitArrayFast])
def test_bad_init(BitArrayClass):
    with pytest.raises(TypeError):
        BitArrayClass(5.5)

    with pytest.raises(TypeError):
        BitArrayClass("hello")

    with pytest.raises(ValueError):
        BitArrayClass(0)

    with pytest.raises(ValueError):
        BitArrayClass(-5)


def test_out_of_range(empty_bit_array):
    with pytest.raises(IndexError):
        empty_bit_array[15] = 1
    with pytest.raises(IndexError):
        empty_bit_array[15] = 0
    with pytest.raises(IndexError):
        empty_bit_array[15]


def test_setitem(empty_bit_array):
    empty_bit_array[0] = 1
    assert empty_bit_array[0] == 1
    empty_bit_array[0] = 0
    assert empty_bit_array[0] == 0


def test_getitem(filled_bit_array):
    assert filled_bit_array[2] == 1
    assert filled_bit_array[5] == 1
    assert filled_bit_array[0] == 0


def test_iter(empty_bit_array):
    for bit in empty_bit_array:
        assert bit == 0


def test_length(filled_bit_array):
    assert len(filled_bit_array) == 10


@pytest.mark.parametrize("BitArrayClass", [BitArray, BitArrayFast])
def test_many_modifications(BitArrayClass):
    bit_array = BitArrayClass(1000)
    for i in range(len(bit_array)):
        bit_array[i] = 1
        assert bit_array[i] == 1

    for i in range(len(bit_array)):
        bit_array[i] = 0
        assert bit_array[i] == 0


@pytest.mark.parametrize("BitArrayClass", [BitArray, BitArrayFast])
def test_or(BitArrayClass):
    SIZE = 20_000
    bit_array_even = BitArrayClass(SIZE)
    bit_array_odd = BitArrayClass(SIZE)
    for i in range(0, SIZE - 1, 2):
        bit_array_even[i] = 1

    for i in range(1, SIZE, 2):
        bit_array_odd[i] = 1

    bit_array_odd.bitwise_or(bit_array_even)

    for i in range(SIZE):
        assert bit_array_odd[i] == 1


@pytest.mark.parametrize("BitArrayClass", [BitArray, BitArrayFast])
def test_prohibited_or(BitArrayClass):
    arr = BitArrayClass(3)

    with pytest.raises(ValueError):
        arr.bitwise_or(BitArrayClass(5))

    with pytest.raises(TypeError):
        arr.bitwise_or([0, 1, 0])


def test_memory():
    # For large sizes, BitArray will be much smaller than a list
    for i in range(500_000, 1_000_001, 100_000):
        lst = [0] * i
        b = BitArray(i)
        assert b.__sizeof__() < lst.__sizeof__() / 60
