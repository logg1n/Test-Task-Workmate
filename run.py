import argparse
import logging
from typing import Tuple, List

from tabulate import tabulate

from script import analysis_of_developer_performance
from reports import Reports


def get_args_command_line() -> Tuple[List[str], str]:
    parser = argparse.ArgumentParser(
        prog="Analysis of developer performance", allow_abbrev=False
    )
    parser.add_argument(
        "--files",
        required=True,
        nargs="+",
        help="Пути к CSV-файлам с данными",
    )
    parser.add_argument(
        "--reports",
        required=True,
        help="Название отчета задает параметры выборки(Регистрозависимый параметр)",
    )

    args = parser.parse_args()

    return args.files, args.reports


def main() -> None:
    files, report = get_args_command_line()

    config = Reports.registry.get(report)
    if not config:
        raise ValueError(f"Неизвестный отчёт: {report}")

    table = analysis_of_developer_performance(files, keys=config["columns"])

    for cb in config["callbacks"]:
        table = cb(table)

    print(tabulate(table.get_rows()[1:], headers=table.get_rows()[0], floatfmt=".2f"))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.exception("Ошибка выполнения программы")
