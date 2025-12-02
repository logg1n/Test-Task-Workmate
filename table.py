"""
Модуль table: универсальная обёртка для работы с табличными данными.
"""

from typing import List, Any


class Table:
    """
    Класс-обёртка для работы с табличными данными.

    Таблица хранится как список списков:
    - первая строка (`rows[0]`) — заголовки колонок,
    - все остальные строки (`rows[1:]`) — данные.
    """

    def __init__(self, headers: List[str]):
        """Создать таблицу с указанными заголовками."""
        self.rows: List[List[Any]] = [headers]

    def add_row(self, row: List[Any]) -> None:
        """Добавить строку данных. Длина строки должна совпадать с количеством заголовков."""
        if len(row) != len(self.rows[0]):
            raise ValueError("Длина строки не совпадает с количеством колонок")
        self.rows.append(row)

    def get_rows(self) -> List[List[Any]]:
        """Вернуть все строки таблицы (заголовки + данные)."""
        return self.rows

    def replace(self, headers: List[str], rows: List[List[Any]]) -> None:
        """Полностью заменить таблицу новыми заголовками и строками."""
        self.rows = [headers] + rows

    @property
    def headers(self) -> List[str]:
        """Вернуть заголовки таблицы (первая строка)."""
        return self.rows[0]

    @property
    def data(self) -> List[List[Any]]:
        """Вернуть все строки данных (без заголовков)."""
        return self.rows[1:]
