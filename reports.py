class Reports:

    @staticmethod
    def count_average(table, column_name: str):
        """Посчитать среднее значение по колонке для каждой уникальной позиции"""
        headers = [col[0] for col in table.matrix]

        if column_name not in headers:
            raise ValueError(f"Колонка '{column_name}' не найдена")

        idx = headers.index(column_name)

        rows = table.get_rows()[1:]  # все строки без заголовков
        result = {}

        for row in rows:
            key = row[0]
            val = row[idx]
            if isinstance(val, list):
                vals = [x for x in val if isinstance(x, (int, float))]
            elif isinstance(val, (int, float)):
                vals = [val]
            else:
                vals = []

            if vals:
                result.setdefault(key, []).extend(vals)

        table.matrix[idx][1] = [
            round(sum(vals) / len(vals), 2) for key, vals in result.items()
        ]

        # первая колонка остаётся только с уникальными ключами
        table.matrix[0][1] = list(result.keys())

        return table

    @staticmethod
    def sort_by_column(table, column_name: str, reverse: bool = True):
        """Отсортировать таблицу по указанной колонке (in-place)"""
        rows = table.get_rows()
        if not rows:
            return table

        headers, data_rows = rows[0], rows[1:]

        if column_name not in headers:
            raise ValueError(f"Колонка '{column_name}' не найдена")

        idx = headers.index(column_name)

        # сортируем все строки целиком по значению в нужной колонке
        sorted_rows = sorted(data_rows, key=lambda r: r[idx], reverse=reverse)

        # очищаем старые значения и заполняем заново
        for i, _ in enumerate(headers):
            table.matrix[i][1] = [row[i] for row in sorted_rows]

        return table
