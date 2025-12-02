# Analysis of developer performance

Скрипт **Analysis of developer performance** предназначен для анализа данных о сотрудниках из CSV‑файлов.  
Он работает через командную строку и позволяет запускать разные отчёты с помощью аргумента `--reports`.

## Демонстрация работы

### Работа скрипта
![Демонстрация работы скрипта](docs/демонстрация%20работы%20скрипта.gif)

### Добавление нового отчёта
[![Добавление нового отчёта]](docs/добавление%20нового%20отчета.mp4)


## Основные шаги работы
1. Считывание CSV‑файлов (`--files`).
2. Преобразование данных в объект `Table`.
3. Загрузка и применение выбранного отчёта из пакета `Reports`.
4. Вывод результата в консоль.

---

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

## Инструкция по добавлению новых отчётов
### 1. Структура проекта
```commandline
D:\github\Analysis of developer performance

├── csv_files/            # входные CSV-файлы с данными сотрудников
├── Reports/              # пакет с отчётами (каждый отчёт — отдельный модуль)
│   ├── __init__.py       # пустой или с описанием пакета
│   ├── performance.py    # отчёт "среднее значение" + сортировка "по убыванию"
│   ├── skills.py         # отчёт "подсчёт навыков"
│   └── ...               # другие отчёты
│
├── Tests/                # тесты для проверки работы системы
│   └── test_reports.py   # примеры unit-тестов для отчётов
│   └── ...               # другие тесты
│
├── README.md             # документация проекта
├── requirements.txt      # зависимости Python
│
├── reports.py            # базовый класс Reports (реестр и загрузка отчётов)
├── run.py                # CLI-скрипт для запуска анализа
├── script.py             # логика анализа производительности (парсинг CSV)
└── table.py              # класс Table — универсальная обёртка для таблиц
```
- Все отчёты находятся в пакете Reports.
- Имя файла должно совпадать с полем name внутри класса отчёта.
- Аргумент --reports в CLI также должен совпадать с этим именем.

### 2. Определите назначение отчёта
Решите, что именно должен делать отчёт: считать среднее, фильтровать данные, строить рейтинг и т.д.

### 3. Напишите класс отчёта
1. Создайте новый файл в пакете Reports/.
2. Имя файла = значение поля name.
3. Оберните класс в декоратор @Reports.register_report.
4. Укажите:
   - name — уникальное имя отчёта,
   - columns — список колонок, которые нужны отчёту,
   - callbacks — список функций‑обработчиков.

Пример (Reports/skills.py):
```python
from report import Reports
from collections import Counter

@Reports.register_report
class CountBySkills:
    name = "skills"
    columns = ["skills"]

    @staticmethod
    def count_by_skill(table, column_name: str = "skills"):
        headers = table.get_rows()[0]
        idx = headers.index(column_name)

        all_skills = []
        for row in table.get_rows()[1:]:
            skills = row[idx]
            if isinstance(skills, str):
                for s in skills.split(","):
                    s = s.strip()
                    if s:
                        all_skills.append(s)

        skill_counts = Counter(all_skills)
        new_rows = [[skill, count] for skill, count in skill_counts.items()]
        table.replace(["skill", "count"], new_rows)

        return table

    callbacks = [count_by_skill]
```

### 4. Запустите отчёт через CLI
Аргумент --reports должен совпадать с именем файла и полем name.
Пример запуска:
```commandline
python main.py --files data.csv --reports skills
```
