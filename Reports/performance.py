"""
Модуль Reports.performance: отчёт для анализа производительности разработчиков.

Содержит класс Performance, который определяет структуру колонок и набор
обработчиков (callbacks) для постобработки таблицы.
"""

from typing import Any

from report import Reports
from table import Table


@Reports.register_report
class Performance:
    """
    Отчёт по производительности разработчиков.

    Содержит методы для:
    - вычисления среднего значения по колонке,
    - сортировки таблицы по указанной колонке.
    """

    name: str = "performance"
    columns: list[str] = ["position", "performance"]

    @staticmethod
    def count_average(
        table: Table,
        column_name: str = "performance",
        group_by: str = "position",
    ) -> Table:
        """Посчитать среднее значение по колонке для каждой уникальной позиции."""
        headers: list[str] = table.headers

        idx_group: int = headers.index(group_by)
        idx_value: int = headers.index(column_name)

        result: dict[str, list[float]] = {}
        for row in table.data:
            key: Any = row[idx_group]
            val: Any = row[idx_value]
            if isinstance(val, (int, float)):
                result.setdefault(key, []).append(val)

        new_rows: list[list[Any]] = [
            [key, round(sum(vals) / len(vals), 2)] for key, vals in result.items()
        ]

        table.replace([group_by, column_name], new_rows)
        return table

    @staticmethod
    def sort_by_column(
        table: Table,
        column_name: str = "performance",
        reverse: bool = True,
    ) -> Table:
        """Отсортировать таблицу по указанной колонке (in-place)."""
        headers: list[str] = table.headers

        idx: int = headers.index(column_name)
        sorted_rows: list[list[Any]] = sorted(
            table.data, key=lambda r: r[idx], reverse=reverse
        )

        table.replace(headers, sorted_rows)
        return table

    callbacks = [count_average, sort_by_column]
