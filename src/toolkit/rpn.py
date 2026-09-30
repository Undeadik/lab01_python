"""Перевод инфиксного выражения в обратную польскую запись (ОПЗ)."""

from .constants import OPERATOR_PRECEDENCE

Token = tuple[str, str]


def to_rpn(tokens: list[Token]) -> list[Token]:
    """Переводит поток токенов из инфиксной записи в ОПЗ.

    Использует shunting-yard.
    Унарные плюс и минус определяются по позиции оператора и 
    выводятся как токены "UNARY", стоящие после своего операнда.
    """
    output: list[Token] = []
    stack: list[Token] = []
    prev_kind: str | None = None

    for kind, value in tokens:
        if kind == "NUMBER":
            output.append((kind, value))
            while stack and stack[-1][0] == "UNARY":
                output.append(stack.pop())

        elif kind == "OPERATOR":
            if _is_unary(prev_kind):
                stack.append(("UNARY", "u" + value))
            else:
                while (
                    stack
                    and stack[-1][0] == "OPERATOR"
                    and OPERATOR_PRECEDENCE[stack[-1][1]]
                    >= OPERATOR_PRECEDENCE[value]
                ):
                    output.append(stack.pop())
                stack.append((kind, value))
        prev_kind = kind

    while stack:
        output.append(stack.pop())

    return output


def _is_unary(prev_kind: str | None) -> bool:
    """Возвращает True, если знак +/- в этой позиции унарный."""
    return prev_kind is None or prev_kind in "OPERATOR"