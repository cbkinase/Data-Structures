import pytest
from src import BloomFilter


@pytest.fixture
def empty_filter():
    return BloomFilter(10_000, fp_rate=0.01)


@pytest.fixture
def inserted_filter():
    f = BloomFilter(10_000, fp_rate=0.01)
    f.put("hello")
    f.put("world")
    return f


def test_may_contain(inserted_filter: BloomFilter):
    assert inserted_filter.may_contain("hello") is True
    assert inserted_filter.may_contain("world") is True


def test_expected_fpp(inserted_filter: BloomFilter):
    assert pytest.approx(inserted_filter.expected_fpp(), abs=10e-5) == 0.01


def test_put_all(inserted_filter: BloomFilter, empty_filter: BloomFilter):
    empty_filter.put_all(inserted_filter)
    assert empty_filter.may_contain("hello") is True
    assert empty_filter.may_contain("world") is True


def test_bad_put_all(inserted_filter: BloomFilter):
    bad_k = BloomFilter(100_000, fp_rate=0.03)
    bad_m = BloomFilter(100_000, fp_rate=0.01)

    with pytest.raises(ValueError):
        inserted_filter.put_all([0, 0, 0])

    with pytest.raises(ValueError):
        inserted_filter.put_all(inserted_filter)

    with pytest.raises(ValueError):
        inserted_filter.put_all(bad_k)

    with pytest.raises(ValueError):
        inserted_filter.put_all(bad_m)

    with pytest.raises(ValueError):
        inserted_filter.put_all(inserted_filter)


def test_in(inserted_filter: BloomFilter):
    assert "world" in inserted_filter


def test_not_in(empty_filter: BloomFilter):
    assert empty_filter.may_contain("hello") is False
