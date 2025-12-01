# Описание скрипта
Скрипт **Analysis of developer performance** предназначен для анализа данных о сотрудниках из CSV‑файлов.  
Он работает через командную строку и позволяет запускать разные отчёты с помощью аргумента `--reports`.  
Основные шаги работы:
1. Считывание CSV‑файлов (`--files`).
2. Преобразование данных в объект `Table`.
3. Применение выбранного отчёта из `Reports.registry`.
4. Вывод результата в консоль.

# Инструкция по добавлению новых отчётов

## Класс `Table`
`Table` — это универсальная обёртка для работы с табличными данными.  
Он хранит строки в виде списка списков, где:
- первая строка (`get_rows()[0]`) — это **заголовки колонок**,
- все остальные строки (`get_rows()[1:]`) — это **данные**.

### Основные методы:
- `Table(headers: list[str])` — создать таблицу с указанными заголовками.
- `add_row(row: list)` — добавить строку данных (длина должна совпадать с количеством заголовков).
- `get_rows() -> list[list]` — получить все строки (включая заголовки).
- `replace(headers: list[str], rows: list[list])` — заменить заголовки и строки новыми.

Пример:
```python
table = Table(["position", "performance"])
table.add_row(["Backend Developer", 4.8])
table.add_row(["QA Engineer", 4.5])

print(table.get_rows())
# [
#   ["position", "performance"],
#   ["Backend Developer", 4.8],
#   ["QA Engineer", 4.5]
# ]
```

## 1. Определите назначение отчёта
- Решите, что именно должен делать отчёт: считать среднее, медиану, фильтровать данные, строить рейтинг и т.д.

## 2. Напишите функцию-обработчик
- Функция принимает объект `Table` и возвращает его же (с изменёнными строками/колонками).
- Пример:
  ```python
    @staticmethod
    def count_by_skill(table, column_name: str = "skills"):
        """Посчитать количество сотрудников по каждому навыку"""

        headers = table.get_rows()[0]
        idx = headers.index(column_name)

        all_skills = []
        for row in table.get_rows()[1:]:  # берём строки без заголовков
            skills = row[idx]
            if isinstance(skills, str):
                for s in skills.split(","):
                    s = s.strip()
                    if s:  # ✅ пропускаем пустые строки
                        all_skills.append(s)

        skill_counts = Counter(all_skills)

        new_rows = [[skill, count] for skill, count in skill_counts.items()]
        table.replace([column_name], new_rows)

        return table
  ```
## 3. Зарегистрируйте отчёт в Reports.registry
- Добавьте новый ключ в словарь:
- Пример:
  ```python
  registry = {
      "performance": {
          "columns": ["position", "performance"],
          "callbacks": [Reports.count_average, Reports.sort_by_column],
      },
      "skills": {
          "columns": ["skills"],
          "callbacks": [Reports.count_by_skill],
      },
  }
  ```
## 4. Запустите отчёт через CLI
- В run.py аргумент --reports должен совпадать с ключом в Reports.registry.
- Пример запуска:
  ```commandline
    python run.py --files data.csv --reports skills
  ```