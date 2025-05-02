import pytest
from yandex_testing_lesson import is_under_queen_attack


def test_valid_positions_under_attack():
    assert is_under_queen_attack("e8", "e1")
    assert is_under_queen_attack("a1", "h8")
    assert is_under_queen_attack("h8", "a1")
    assert is_under_queen_attack("e1", "e8")
    assert is_under_queen_attack("e1", "e1")


def test_valid_positions_not_under_attack():
    assert not is_under_queen_attack("b4", "a2")
    assert not is_under_queen_attack("f4", "h8")


def test_invalid_input_format():
    with pytest.raises(ValueError):
        is_under_queen_attack("j5", "e4")
    with pytest.raises(ValueError):
        is_under_queen_attack("e4", "j5")
    with pytest.raises(ValueError):
        is_under_queen_attack("abc", "e4")
    with pytest.raises(ValueError):
        is_under_queen_attack("e4", "abc")
    with pytest.raises(ValueError):
        is_under_queen_attack("a9", "e4")
    with pytest.raises(ValueError):
        is_under_queen_attack("e4", "a9")
    with pytest.raises(ValueError):
        is_under_queen_attack("e4", "34")
    with pytest.raises(ValueError):
        is_under_queen_attack("34", "e4")
    with pytest.raises(ValueError):
        is_under_queen_attack("e4", "a")
    with pytest.raises(ValueError):
        is_under_queen_attack("a", "e4")


def test_invalid_input_type():
    with pytest.raises(TypeError):
        is_under_queen_attack('e4', None)
    with pytest.raises(TypeError):
        is_under_queen_attack(None, 'e4')
    with pytest.raises(TypeError):
        is_under_queen_attack(42, 42)
    with pytest.raises(TypeError):
        is_under_queen_attack(42, "e4")
    with pytest.raises(TypeError):
        is_under_queen_attack("e4", 42)
    with pytest.raises(TypeError):
        is_under_queen_attack(42.36, "e4")
    with pytest.raises(TypeError):
        is_under_queen_attack("e4", 42.36)
    with pytest.raises(TypeError):
        is_under_queen_attack(["e", "4"], "e4")
    with pytest.raises(TypeError):
        is_under_queen_attack("e4", ["e", "4"])
    with pytest.raises(TypeError):
        is_under_queen_attack({}, "e4")
    with pytest.raises(TypeError):
        is_under_queen_attack("e4", {})