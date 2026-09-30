"""Точка входа CLI пакета toolkit."""

import argparse
import sys

from .calculator import calculate
from .converter import convert
from .errors import ToolkitError


def build_parser() -> argparse.ArgumentParser:
    """Собирает главный парсер аргументов."""
    parser = argparse.ArgumentParser(
        prog="toolkit",
        description="CLI toolkit: калькулятор и конвертер единиц",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    calc_p = sub.add_parser("calc", help="Вычислить выражение")
    calc_p.add_argument(
        "expression",
        type=str,
        help='Выражение, например "2+3*4"',
    )

    conv_p = sub.add_parser("convert", help="Перевести единицы")
    conv_p.add_argument("value", type=float, help="Числовое значение")
    conv_p.add_argument(
        "--from", dest="from_unit", required=True, help="Исходная единица"
    )
    conv_p.add_argument(
        "--to", dest="to_unit", required=True, help="Целевая единица"
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    """Запускает CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "calc":
            print(calculate(args.expression))
        elif args.command == "convert":
            print(convert(args.value, args.from_unit, args.to_unit))
    except ToolkitError as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        return 2

    return 0