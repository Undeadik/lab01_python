"""Токенизация арифметических выражений."""

import re

from .errors import CalculatorError

# Тип одного токена: кортеж из двух строк (тип, значение).
Token = tuple[str, str]

# Регулярка для поиска токенов. 
TOKEN_RE = re.compile(
    r"""
    (?P<NUMBER>\d+(?:\.\d+)?)   
  | (?P<OPERATOR>//|[%+\-*/])        
    """,
    re.VERBOSE,
)


def tokenize(exp: str) -> list[Token]:
    """Разбивает выражение на типизированные токены."""
    tokens: list[Token] = []
    last_end = 0

    for match in TOKEN_RE.finditer(exp):
        gap = exp[last_end:match.start()]
        if gap.strip():
            raise CalculatorError(f"Недопустимый символ: {gap!r}")

        kind = match.lastgroup
        tokens.append((kind, match.group(kind)))
        last_end = match.end()

    tail = exp[last_end:]
    if tail.strip():
        raise CalculatorError(f"Недопустимый символ: {tail!r}")

    return tokens