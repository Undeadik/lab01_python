"""Тесты CLI через subprocess."""

import subprocess
import sys


def run_cli(args: list[str]) -> subprocess.CompletedProcess[str]:
    """Запускает python -m toolkit с указанными аргументами."""
    return subprocess.run(
        [sys.executable, "-m", "toolkit", *args],
        capture_output=True,
        text=True,
    )


def test_calc_success() -> None:
    """Calc возвращает 0 и печатает результат."""
    res = run_cli(["calc", "2+3*4"])
    assert res.returncode == 0
    assert res.stdout.strip() == "14"


def test_convert_success() -> None:
    """Convert возвращает 0 и печатает результат."""
    res = run_cli(["convert", "100", "--from", "cm", "--to", "m"])
    assert res.returncode == 0
    assert res.stdout.strip() == "1.0"


def test_error_go_to_stderr() -> None:
    """Ошибка пользователя: код 2 и сообщение в stderr."""
    res = run_cli(["calc", "1/0"])
    assert res.returncode == 2
    assert "Ошибка" in res.stderr


def test_calc_missing_argument() -> None:
    """Calc без выражения: код 2."""
    res = run_cli(["calc"])
    assert res.returncode == 2
    assert "error" in res.stderr.lower()


def test_unknown_command() -> None:
    """Неизвестная команда возвращает 2."""
    res = run_cli(["unknown"])
    assert res.returncode == 2


def test_help_exit_code_zero() -> None:
    """--help возвращает 0."""
    res = run_cli(["--help"])
    assert res.returncode == 0