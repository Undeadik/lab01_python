"""Ядро конвертера единиц: длина, масса, температура."""

from .constants import ABSOLUTE_ZERO, UNITS
from .errors import ConverterError
from .validator import validate_units


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """Перевод значений."""
    from_unit, to_unit = validate_units(from_unit, to_unit)

    group_from, factor_from = UNITS[from_unit]
    group_to, factor_to = UNITS[to_unit]

    if group_from == "temp":
        cels = _to_cels(value, from_unit)
        if cels < ABSOLUTE_ZERO:
            raise ConverterError("Температура ниже абсолютного нуля")
        return _from_cels(cels, to_unit)

    assert factor_from is not None
    assert factor_to is not None
    base_value = value*factor_from
    return base_value/factor_to


def _to_cels(value: float, unit: str) -> float:
    """Переводит температуру в Цельсий."""
    if unit == "c":
        return value
    if unit == "f":
        return (value-32)*5/9
    if unit == "k":
        return value - 273.15
    raise ConverterError(f"Неизвестная единица температуры: {unit}")


def _from_cels(cels: float, unit: str) -> float:
    """Переводит температуру из Цельсия в целевую единицу."""
    if unit == "c":
        return cels
    if unit == "f":
        return cels * 9/5+32
    if unit == "k":
        return cels + 273.15
    raise ConverterError(f"Неизвестная единица температуры: {unit}")