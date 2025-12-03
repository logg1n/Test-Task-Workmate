"""
Модуль Reports.skills: отчёт для анализа навыков разработчиков.

Содержит класс Skills, который определяет структуру колонок и набор
обработчиков (callbacks) для постобработки таблицы.
"""

from collections import Counter
from typing import Any
from report import Reports
from table import Table


@Reports.register_report
class CountBySkills:
    """
    Отчёт по навыкам сотрудников.

    Считает количество сотрудников по каждому уникальному навыку,
    найденному в колонке "skills".
    """

    name: str = "skills"
    columns: list[str] = ["skills"]

    @staticmethod
    def count_by_skill(table: Table, column_name: str = "skills") -> Table:
        """Посчитать количество сотрудников по каждому навыку."""

        # собираем все навыки в один список
        all_skills: list[str] = [
            s.strip()
            for skills in table["skills"] if isinstance(skills, str)
            for s in skills.split(",")
            if s.strip()
        ]

        # считаем количество уникальных навыков
        skill_counts: Counter[str] = Counter(all_skills)

        # формируем новые строки
        new_rows: list[list[Any]] = [
            [skill, count] for skill, count in skill_counts.items()
        ]
        table.replace([column_name], new_rows)

        return table

    callbacks = [count_by_skill]
