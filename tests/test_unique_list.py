import pytest
from src import UniqueList


@pytest.fixture
def unique():
    u = UniqueList()
    u.append("hello")
    u.append("world")
    return u


def test_get_length(unique: UniqueList):
    assert len(unique) == 2


def test_get_at(unique: UniqueList):
    assert unique[0] == "hello"


def test_set_at(unique: UniqueList):
    unique[0] = "yes"
    assert unique[0] == "yes"


def test_invalid_set_at(unique: UniqueList):
    with pytest.raises(ValueError):
        unique[0] = "world"


def test_contains_valid(unique: UniqueList):
    assert "hello" in unique


def test_contains_invalid(unique: UniqueList):
    assert "blasphemy" not in unique


def test_append(unique: UniqueList):
    unique.append("general")
    assert unique[-1] == "general"


def test_repeat_append(unique: UniqueList):
    unique.append("hello")
    assert len(unique) == 2


def test_strict_append(unique: UniqueList):
    with pytest.raises(ValueError):
        unique.append("hello", strict=True)


def test_strict_append_allowed(unique: UniqueList):
    unique.append("general")
    assert unique[-1] == "general"


def test_clear(unique: UniqueList):
    unique.clear()
    assert len(unique) == 0


def test_bool(unique: UniqueList):
    assert bool(unique) is True
    assert bool(UniqueList()) is False


def test_reverse(unique: UniqueList):
    unique.reverse()
    assert unique[0] == "world"
    assert unique[1] == "hello"


def test_repr(unique: UniqueList):
    assert type(repr(unique)) == str
    assert "hello" in repr(unique)


def test_pop(unique: UniqueList):
    unique.pop()
    assert len(unique) == 1
    assert unique[0] == "hello"


def test_pop_with_index(unique: UniqueList):
    unique.pop(0)
    assert len(unique) == 1
    assert unique[0] == "world"


def test_remove(unique: UniqueList):
    unique.remove("hello")
    assert len(unique) == 1
    assert unique[0] == "world"


def test_remove_invalid(unique: UniqueList):
    with pytest.raises(ValueError):
        unique.remove("blasphemy")


def test_constructor_with_iterable():
    unique = UniqueList([1, 2, 3, 4])
    assert len(unique) == 4
    assert unique[-1] == 4


def test_constructor_with_duplicates():
    unique = UniqueList([1, 2, 3, 4, 1])
    assert len(unique) == 4
    assert unique[-1] == 4


def test_extend(unique: UniqueList):
    unique.extend(["electric", "city"])
    assert len(unique) == 4
    assert unique[-1] == "city"


def test_with_tuples():
    unique = UniqueList([(1, 2), (2, 3), (1, 2)])
    unique.append((1, 2))
    assert len(unique) == 2


def test_insert(unique: UniqueList):
    unique.insert(0, "goodbye")
    assert unique[0] == "goodbye"


def test_insert_repeat(unique: UniqueList):
    unique.insert(0, "world")
    assert unique[0] == "hello"


def test_insert_repeat_strict(unique: UniqueList):
    with pytest.raises(ValueError):
        unique.insert(0, "world", strict=True)


def test_insert_strict_allowed(unique: UniqueList):
    unique.insert(0, "goodbye", strict=True)
    assert unique[0] == "goodbye"


def test_delete(unique: UniqueList):
    del unique[0]
    assert unique[0] == "world"


def test_reversed(unique: UniqueList):
    rev = reversed(unique)
    assert UniqueList(rev)[0] == "world"
