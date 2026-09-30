"""Пользовательские исключения пакета toolkit."""


class ToolkitError(Exception):
    """Базовое исключение для всех ошибок toolkit."""


class CalculatorError(ToolkitError):
    """Ошибка в выражении калькулятора."""


class ConverterError(ToolkitError):
    """Ошибка при конвертации единиц."""