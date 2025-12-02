"""
Модуль report: базовый класс Reports для регистрации и загрузки отчётов.
"""

import importlib
from typing import Any, Dict, Type


class Reports:
    """
    Реестр отчётов.

    Позволяет регистрировать классы отчётов и загружать их по имени.
    Каждый отчёт хранится в виде словаря с ключами:
    - "columns": список колонок, которые отчёт добавляет или использует,
    - "callbacks": список функций-обработчиков, применяемых к таблице.
    """

    registry: Dict[str, Dict[str, Any]] = {}

    @staticmethod
    def register_report(cls: Type) -> Type:
        """
        Зарегистрировать класс отчёта в реестре.
        Args:
            cls (Type): класс отчёта, у которого должны быть атрибуты
                name (str), columns (List[str]) и callbacks (List[callable]).
        Returns:
            Type: тот же класс, чтобы можно было использовать как декоратор.
        """

        Reports.registry[cls.name] = {
            "columns": getattr(cls, "columns", []),
            "callbacks": getattr(cls, "callbacks", []),
        }
        return cls

    @staticmethod
    def load_report(report_name: str) -> Dict[str, Any]:
        """
        Импортировать модуль отчёта по имени и вернуть его конфигурацию.
        Args:
            report_name (str): имя отчёта (совпадает с названием файла в пакете Reports).
        Returns:
            Dict[str, Any]: словарь с ключами "columns" и "callbacks".
        Raises:
            RuntimeError: если отчёт не зарегистрирован.
        """

        importlib.import_module(f"Reports.{report_name}")

        if report_name not in Reports.registry:
            raise RuntimeError(f"Отчёт '{report_name}' не зарегистрирован")

        return Reports.registry[report_name]
