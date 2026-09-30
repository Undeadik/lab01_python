"""Тесты ядра конвертера."""

import pytest

from toolkit.converter import convert
from toolkit.errors import ConverterError

# позитивные тесты

def test_mm_to_m() -> None:
    """1000 mm == 1 m."""
    assert convert(1000, "mm", "m") == 1.0


def test_kg_to_g() -> None:
    """1.5 kg == 1500 g."""
    assert convert(1.5, "kg", "g") == 1500.0


def test_c_to_f() -> None:
    """0 C == 32 F."""
    assert convert(0, "c", "f") == 32.0


def test_cels_to_kelvin_absolute_zero() -> None:
    """-273.15 C - 0 K примерно."""
    assert abs(convert(-273.15, "c", "k")) < 1e-9


def test_units_case_insensitive() -> None:
    """Регистр единиц не важен."""
    assert convert(100, "CM", "M") == 1.0


# негативные тесты

def test_below_absolute_zero() -> None:
    """Температура ниже абсолютного нуля."""
    with pytest.raises(ConverterError):
        convert(-300, "c", "k")


def test_incompatible_units() -> None:
    """Разные группы."""
    with pytest.raises(ConverterError):
        convert(1, "m", "kg")


def test_unknown_unit1() -> None:
    """Перевод в неизевстную единиицу."""
    with pytest.raises(ConverterError):
        convert(1, "m", "xyz")


def test_unknown_unit2() -> None:
    """Перевод из неизвестной единиицы."""
    with pytest.raises(ConverterError):
        convert(1, "pikmi", "k")