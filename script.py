"""
Содержит функцию analysis_of_developer_performance, которая загружает данные
из CSV‑файлов и формирует объект Table для дальнейшей обработки отчётами.
"""

import csv
import re
from typing import List, Optional
from table import Table


def analysis_of_developer_performance(
    files: List[str], keys: Optional[List[str]] = None
) -> Optional[Table]:
    """
    Загружает данные из CSV‑файлов и формирует таблицу.

    Args:
        files (list[str]): пути к CSV‑файлам с данными.
        keys (list[str] | None): список колонок, которые нужно извлечь.
            Если None — берутся все заголовки из файла.

    Returns:
        Table | None: объект Table с заголовками и строками,
        либо None, если список файлов пуст.
    """

    pattern = re.compile(r"^-?\d+(?:\.\d+)?$")
    table: Optional[Table] = None

    for file in files:
        with open(file, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            headers = next(reader)

            if not keys:
                valid_keys = headers
            else:
                valid_keys = [k for k in keys if k in headers]

            if table is None:
                table = Table(valid_keys)

            indexes = [headers.index(v) for v in valid_keys]

            if not indexes:
                continue

            for row in reader:
                values = [
                    float(v) if pattern.match(v) else v
                    for v in (row[i] for i in indexes)
                ]
                table.add_row(values)

    return table
