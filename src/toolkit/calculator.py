"""Вычисление ОПЗ и точка входа калькулятора."""

from .errors import CalculatorError
from .rpn import to_rpn
from .tokenizer import Token, tokenize
from .validator import validate


def evaluate_rpn(rpn: list[Token]) -> int | float:
    """Вычисляет поток токенов в ОПЗ с помощью стека."""
    stack: list[float | int] = []

    for kind, value in rpn:
        if kind == "NUMBER":
            if "." in value:
                stack.append(float(value))
            else:
                stack.append(int(value))

        elif kind == "UNARY":
            operand = stack.pop()
            stack.append(operand if value == "u+" else -operand)

        elif kind == "OPERATOR":
            right = stack.pop()
            left = stack.pop()
            stack.append(_apply_binary(value, left, right))

        else:
            raise CalculatorError(f"Неизвестный тип токена: {kind}")

    if len(stack) != 1:
        raise CalculatorError("Некорректное выражение")
    return stack[0]


def calculate(exp: str) -> float | int:
    """Вычисляет арифметическое выражение и возвращает результат."""
    tokens = tokenize(exp)
    validate(tokens)
    rpn = to_rpn(tokens)
    return evaluate_rpn(rpn)


def _apply_binary(op: str, left: int | float, right: int | float) -> int | float:
    """Применяет бинарный оператор к двум операндам."""
    if op == "+":
        return left + right
    if op == "-":
        return left - right
    if op == "*":
        return left * right
    if op == "/":
        if right == 0:
            raise CalculatorError("Деление на ноль")
        return left / right
    if op == "%":
        if right == 0:
            raise CalculatorError("Деление на ноль")
        return left % right
    if op == "//":
        if right == 0:
            raise CalculatorError("Деление на ноль")
        return left // right
    raise CalculatorError(f"Неизвестный оператор: {op}")