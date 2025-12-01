from collections import Counter


class Reports:
    @staticmethod
    def count_average(
        table, column_name: str = "performance", group_by: str = "position"
    ):
        """Посчитать среднее значение по колонке для каждой уникальной позиции"""
        headers = table.get_rows()[0]

        idx_group = headers.index(group_by)
        idx_value = headers.index(column_name)

        result = {}
        for row in table.get_rows()[1:]:
            key = row[idx_group]
            val = row[idx_value]
            if isinstance(val, (int, float)):
                result.setdefault(key, []).append(val)

        new_rows = [
            [key, round(sum(vals) / len(vals), 2)] for key, vals in result.items()
        ]

        table.replace([group_by, column_name], new_rows)
        return table

    @staticmethod
    def sort_by_column(table, column_name: str = "performance", reverse: bool = True):
        """Отсортировать таблицу по указанной колонке (in-place)"""

        headers = table.get_rows()[0]

        idx = headers.index(column_name)
        sorted_rows = sorted(
            table.get_rows()[1:], key=lambda r: r[idx], reverse=reverse
        )

        table.replace(headers, sorted_rows)
        return table

    @staticmethod
    def count_by_skill(table, column_name: str = "skills"):
        """Посчитать количество сотрудников по каждому навыку"""

        headers = table.get_rows()[0]
        idx = headers.index(column_name)

        # собираем все навыки в один список
        all_skills = []
        for row in table.get_rows()[1:]:  # берём строки без заголовков
            skills = row[idx]
            if isinstance(skills, str):
                for s in skills.split(","):
                    s = s.strip()
                    if s:  # ✅ пропускаем пустые строки
                        all_skills.append(s)

        # считаем количество уникальных навыков
        skill_counts = Counter(all_skills)

        # формируем новые строки
        new_rows = [[skill, count] for skill, count in skill_counts.items()]
        table.replace([column_name], new_rows)

        return table

    registry = {
        "performance": {
            "columns": ["position", "performance"],
            "callbacks": [count_average, sort_by_column],
        },
        "skills": {
            "columns": ["skills"],
            "callbacks": [count_by_skill],
        },
    }
