"""Общие фикстуры для тестов toolkit."""

import pytest


@pytest.fixture
def simple_exp() -> str:
    """Простое выражение."""
    return "2+3*4"


@pytest.fixture
def exp_with_unary() -> str:
    """Выражение с унарными минусами."""
    return "-  2 * - 3"


@pytest.fixture
def length_in_cm() -> float:
    """Длина в сантиметрах."""
    return 100.0
