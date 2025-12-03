"""
Модуль table: универсальная обёртка для работы с табличными данными.
"""

from typing import List, Any, Collection, Iterator, Union


class Table(Collection):
    """
    Класс-обёртка для работы с табличными данными.

    Таблица хранится как список списков:
    - первая строка (`rows[0]`) — заголовки колонок
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

    def is_empty(self)-> bool:
        return not self.data

    def __len__(self) -> int:
        return len(self.data)

    def __contains__(self, item) -> bool:
        return any(item in row for row in self.data)

    def __iter__(self)-> Iterator[List[Any]]:
        return iter(self.data)

    def __getitem__(self, key: Union[int, str]) -> List[Any]:
        if isinstance(key, int):
            return self.data[key]
        elif isinstance(key, str):
            idx = self.headers.index(key)
            return [row[idx] for row in self.data]
        else:
            raise TypeError("Ключ должен быть int или str")

    def __bool__(self) -> bool:
        return len(self.data) > 0
