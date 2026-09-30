"""Валидация потока токенов для калькулятора."""

from .constants import UNITS
from .errors import CalculatorError, ConverterError

Token = tuple[str, str]


def validate(tokens: list[Token]) -> None:
    """Проверяет, что поток токенов — корректное арифметическое выражение."""
    if not tokens:
        raise CalculatorError("Пустое выражение")

    prev: Token | None = None

    for index, (kind, value) in enumerate(tokens):
        if kind == "NUMBER":
            _check_number(prev, index)
        elif kind == "OPERATOR":
            _check_operator(prev, value, index)
        else:
            raise CalculatorError(f"Неизвестный тип токена: {kind}")

        prev = (kind, value)

    # выражение не должно заканчиваться оператором
    if prev is not None and prev[0] == "OPERATOR":
        raise CalculatorError("Выражение заканчивается оператором")

def _check_number(prev: Token | None, index: int) -> None:
    """Проверяет, что число не идёт сразу после числа."""
    if prev is not None and prev[0] == "NUMBER":
        raise CalculatorError(
            f"Два числа подряд на позиции {index}"
        )


def _check_operator(prev: Token | None, value: str, index: int) -> None:
    """Проверяет, что оператор стоит в допустимой позиции."""
    if prev is None:
        if value not in "+-":
            raise CalculatorError(
                f"Выражение начинается с '{value}'"
            )
        return

    if prev[0] == "OPERATOR":
        if value not in "+-":
            raise CalculatorError(
                f"Два бинарных оператора подряд на позиции {index}"
            )
        return


def validate_units(from_unit: str, to_unit: str) -> tuple[str, str]:
    """Проверяет, что единицы известны и совместимы."""
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    if from_unit not in UNITS:
        raise ConverterError(f"Неизвестная единица: {from_unit}")
    if to_unit not in UNITS:
        raise ConverterError(f"Неизвестная единица: {to_unit}")
    group_from, _ = UNITS[from_unit]
    group_to, _ = UNITS[to_unit]
    if group_from != group_to:
        raise ConverterError(
            f"Несовместимые единицы: {from_unit} и {to_unit}"
        )
    return from_unit, to_unit