"""
CLI‑скрипт для запуска анализа производительности разработчиков.
"""

import argparse
import logging
import sys
from typing import Tuple, List

from tabulate import tabulate
from script import analysis_of_developer_performance

from report import Reports


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def get_args_command_line() -> Tuple[List[str], str]:
    """
    Разобрать аргументы командной строки.

    Returns:
        Tuple[List[str], str]: список путей к CSV‑файлам (--files)
        и название отчёта (--reports).
    """
    parser = argparse.ArgumentParser(
        prog="Analysis of developer performance", allow_abbrev=False
    )
    parser.add_argument(
        "--files",
        required=True,
        nargs="+",
        help="Пути к CSV‑файлам с данными",
    )
    parser.add_argument(
        "--reports",
        required=True,
        help="Название отчёта (регистрозависимый параметр)",
    )

    args = parser.parse_args()
    return args.files, args.reports


def main() -> None:
    """Точка входа для CLI‑скрипта."""
    files, report = get_args_command_line()

    config = Reports.load_report(report)

    logging.info("Запускаем отчёт: %s", report)

    table = analysis_of_developer_performance(files, keys=config["columns"])

    rows = table.get_rows()
    if not rows or len(rows) < 2:
        raise ValueError("Таблица пуста или содержит только заголовки.")

    for cb in config["callbacks"]:
        table = cb(table)

    print(tabulate(table.data, headers=table.headers, floatfmt=".2f"))


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, ImportError, ValueError) as e:
        logging.error("Ошибка: %s", e)
        sys.exit(1)
