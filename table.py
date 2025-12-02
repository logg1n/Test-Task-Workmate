from typing import List, Any


class Table:
    """
    Класс-обёртка для работы с табличными данными.

    Таблица хранится как список списков:
    - первая строка (`rows[0]`) — заголовки колонок,
    - все остальные строки (`rows[1:]`) — данные.

    Основные возможности:
    - создание таблицы с заданными заголовками,
    - добавление строк с проверкой длины,
    - получение всех строк (заголовки + данные),
    - полная замена заголовков и строк.

    Пример использования:
        >>> table = Table(["position", "performance"])
        >>> table.add_row(["Backend Developer", 4.8])
        >>> table.add_row(["QA Engineer", 4.5])
        >>> table.get_rows()
        [
            ["position", "performance"],
            ["Backend Developer", 4.8],
            ["QA Engineer", 4.5]
        ]
    """

    def __init__(self, headers: List[str]):
        self.rows: List[List[Any]] = [headers]

    def add_row(self, row: List[Any]) -> None:
        if len(row) != len(self.rows[0]):
            raise ValueError("Длина строки не совпадает с количеством колонок")
        self.rows.append(row)

    def get_rows(self) -> List[List[Any]]:
        return self.rows

    def replace(self, headers: List[str], rows: List[List[Any]]) -> None:
        self.rows = [headers] + rows

    @property
    def headers(self) -> List[str]:
        """Вернуть заголовки таблицы (первая строка)."""
        return self.rows[0]

    @property
    def data(self) -> List[List[Any]]:
        """Вернуть все строки данных (без заголовков)."""
        return self.rows[1:]
