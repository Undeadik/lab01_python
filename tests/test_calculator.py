"""Тесты ядра калькулятора."""

import pytest

from toolkit.calculator import calculate, evaluate_rpn
from toolkit.errors import CalculatorError
from toolkit.rpn import to_rpn
from toolkit.tokenizer import tokenize

# --- to_rpn ---

def test_to_rpn_simple(simple_exp: str) -> None:
    """2+3*4 → 2 3 4 * +."""
    tokens = tokenize(simple_exp)
    rpn = to_rpn(tokens)
    assert rpn == [
        ("NUMBER", "2"),
        ("NUMBER", "3"),
        ("NUMBER", "4"),
        ("OPERATOR", "*"),
        ("OPERATOR", "+"),
    ]


def test_to_rpn_unary(exp_with_unary: str) -> None:
    """-2*-3 → 2 u- 3 u- *."""
    tokens = tokenize(exp_with_unary)
    rpn = to_rpn(tokens)
    assert rpn == [
        ("NUMBER", "2"),
        ("UNARY", "u-"),
        ("NUMBER", "3"),
        ("UNARY", "u-"),
        ("OPERATOR", "*"),
    ]


# --- evaluate_rpn ---

def test_evaluate_rpn_simple() -> None:
    """2 3 + == 5."""
    rpn = [("NUMBER", "2"), ("NUMBER", "3"), ("OPERATOR", "+")]
    assert evaluate_rpn(rpn) == 5


def test_evaluate_rpn_unary() -> None:
    """4 u- == -4."""
    rpn = [("NUMBER", "4"), ("UNARY", "u-")]
    assert evaluate_rpn(rpn) == -4


def test_evaluate_rpn_by_zero_n1() -> None:
    """1 0 / ошибка."""
    rpn = [("NUMBER", "1"), ("NUMBER", "0"), ("OPERATOR", "/")]
    with pytest.raises(CalculatorError):
        evaluate_rpn(rpn)


def test_evaluate_rpn_by_zero_n2() -> None:
    """1 0 % ошибка."""
    rpn = [("NUMBER", "1"), ("NUMBER", "0"), ("OPERATOR", "%")]
    with pytest.raises(CalculatorError):
        evaluate_rpn(rpn)


def test_evaluate_rpn_by_zero_n3() -> None:
    """1 0 // ошибка."""
    rpn = [("NUMBER", "1"), ("NUMBER", "0"), ("OPERATOR", "//")]
    with pytest.raises(CalculatorError):
        evaluate_rpn(rpn)


# --- calculate ---

def test_addition() -> None:
    """2+2 == 4."""
    assert calculate("2+2") == 4


def test_precedence(simple_exp: str) -> None:
    """Умножение идёт раньше сложения."""
    assert calculate(simple_exp) == 14


def test_div_is_float() -> None:
    """10/4 == 2.5."""
    assert calculate("10 / 4") == 2.5


def test_unary_minus_both_sides(exp_with_unary: str) -> None:
    """-2*-3 == 6."""
    assert calculate(exp_with_unary) == 6


def test_whitespace_ignored() -> None:
    """Пробелы не ломают разбор."""
    assert calculate("  1 +  2 * 3  ") == 7


def test_unary_after_binary() -> None:
    """1+-2 == -1."""
    assert calculate("1+-2") == -1


def test_integer_division() -> None:
    """7//2 == 3."""
    assert calculate("7//2") == 3


def test_mod() -> None:
    """7%2 == 1."""
    assert calculate("7%2") == 1


def test_double_unary_minus() -> None:
    """--4 == 4."""
    assert calculate("--4") == 4


def test_many_unary_minus_and_plus() -> None:
    """-+-- -- + 4 == -4."""
    assert calculate("-+----+4") == -4


def test_insignificant_zero() -> None:
    """0000000123+5 == 123+5."""
    assert calculate("0000000123+5") == 128


def test_hard_expression() -> None:
    """Выражение со всеми операторами + int и float вместе + унарныe знаки."""
    assert calculate("-3312++23226++55/6-9.9999*+8-+7--0.9999") == pytest.approx(19837.167366666667)

# --- негативные ---

def test_empty_expression() -> None:
    """Пустая строка."""
    with pytest.raises(CalculatorError):
        calculate("")


def test_invalid_character() -> None:
    """Неизвестный символ."""
    with pytest.raises(CalculatorError):
        calculate("222-a")


def test_two_operators() -> None:
    """Два несовместимых оператора."""
    with pytest.raises(CalculatorError):
        calculate("8*/1")


def test_two_numbers_in_a_row() -> None:
    """Два операнда подряд без оператора."""
    with pytest.raises(CalculatorError):
        calculate("1 23")


def test_trailing_operator() -> None:
    """Выражение заканчивается оператором."""
    with pytest.raises(CalculatorError):
        calculate("5-")