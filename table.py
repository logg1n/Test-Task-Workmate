class Table:
    def __init__(self, columns: list[str] = None):
        self.matrix = self.create_matrix(columns) if columns else []

    def create_matrix(self, columns: list[str]):
        """Создать матрицу вида [[название, []], ...]"""
        return [[col, []] for col in columns]

    def add_row(self, row: list):
        """Добавить строку: первая колонка — ключ, остальные значения"""
        if not self.matrix:
            raise ValueError("Сначала нужно создать колонки")

        if len(row) != len(self.matrix):
            raise ValueError(
                "Количество значений должно совпадать с количеством колонок"
            )

        key = row[0]

        # ищем, есть ли уже такой ключ
        if key in self.matrix[0][1]:
            idx = self.matrix[0][1].index(key)
            # добавляем значения в соответствующие списки
            for i in range(1, len(row)):
                self.matrix[i][1][idx].append(row[i])
        else:
            # добавляем новый ключ
            self.matrix[0][1].append(key)
            for i in range(1, len(row)):
                # сразу кладём значение как список
                self.matrix[i][1].append([row[i]])

    def add_column(self, name: str, values: list = None):
        """Добавить новую колонку"""
        self.matrix.append([name, values or []])

    def get_rows(self):
        """Вернуть таблицу построчно"""
        headers = [col[0] for col in self.matrix]
        rows = list(zip(*[col[1] for col in self.matrix]))
        return [headers] + list(rows)
