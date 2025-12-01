import argparse
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
        default="performance",
        help="Название отчета (по умолчанию: performance)",
    )

    args = parser.parse_args()

    return args.files, args.reports


def main() -> None:
    files, report = get_args_command_line()
    columns = ["position", "performance"]
    table = analysis_of_developer_performance(
        files,
        lambda t: Reports.count_average(t, "performance"),
        lambda t: Reports.sort_by_column(t, "performance"),
        keys=columns,
    )

    rows = table.get_rows()
    print("*" * len(f"* report: {report} *"))
    print(f"* report: {report} *")
    print("*" * len(f"* report: {report} *"))
    print(tabulate(rows[1:], headers=rows[0], floatfmt=".2f"))


if __name__ == "__main__":
    main()
