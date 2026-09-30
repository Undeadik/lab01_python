"""Константы пакета toolkit."""

from typing import Final

UNITS: Final[dict[str, tuple[str, float | None]]] = {
    "mm": ("length", 0.001),
    "cm": ("length", 0.01),
    "m": ("length", 1.0),
    "km": ("length", 1000.0),
    "g": ("mass", 1.0),
    "kg": ("mass", 1000.0),
    "c": ("temp", None),
    "f": ("temp", None),
    "k": ("temp", None),
}

ABSOLUTE_ZERO: Final[float] = -273.15

# Приоритеты операторов.
OPERATOR_PRECEDENCE: Final[dict[str, int]] = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
    "%": 2,
    "//": 2,
    "u+": 3,
    "u-": 3,
}