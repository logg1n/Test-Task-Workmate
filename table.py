class Table:
    def __init__(self, headers: list[str]):
        self.rows: list[list] = [headers]

    def add_row(self, row: list):
        """Добавить строку в таблицу"""
        if len(row) != len(self.rows[0]):
            raise ValueError("Длина строки не совпадает с количеством колонок")
        self.rows.append(row)

    def get_rows(self) -> list[list]:
        """Вернуть все строки (заголовки + данные)"""
        return self.rows

    def replace(self, headers: list[str], rows: list[list]):
        """Полностью заменить таблицу новыми заголовками и строками"""
        self.rows = [headers] + rows
