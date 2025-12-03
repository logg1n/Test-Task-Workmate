import tempfile
import csv
import pytest

from script import analysis_of_developer_performance
from table import Table


def create_csv_file(headers, rows):
    with tempfile.NamedTemporaryFile(
        mode="w+", newline="", delete=False, encoding="utf-8"
    ) as tmp:
        writer = csv.writer(tmp)
        writer.writerow(headers)
        writer.writerows(rows)
        tmp.flush()
    return tmp.name


def test_analysis_basic():
    file = create_csv_file(
        ["position", "performance"],
        [["Backend Developer", "4.8"], ["QA Engineer", "4.5"]],
    )
    table = analysis_of_developer_performance([file], keys=["position", "performance"])
    assert table.get_rows() == [
        ["position", "performance"],
        ["Backend Developer", 4.8],
        ["QA Engineer", 4.5],
    ]


def test_analysis_no_keys():
    file = create_csv_file(["position", "performance"], [["Backend Developer", "4.8"]])
    table = analysis_of_developer_performance([file], keys=["Salary"])
    # таблица создаётся с пустыми заголовками
    assert table.get_rows() == [[]]
    assert table.get_rows()[0] == []


def test_analysis_multiple_files():
    file1 = create_csv_file(["position", "performance"], [["Backend Developer", "4.8"]])
    file2 = create_csv_file(["position", "performance"], [["QA Engineer", "4.5"]])
    table = analysis_of_developer_performance(
        [file1, file2], keys=["position", "performance"]
    )
    rows = table.get_rows()
    assert rows == [
        ["position", "performance"],
        ["Backend Developer", 4.8],
        ["QA Engineer", 4.5],
    ]


def test_analysis_empty_files():
    # если список файлов пуст → возвращается None
    table = analysis_of_developer_performance([], keys=["position", "performance"])
    assert table is None


def test_analysis_with_numeric_and_text():
    file = create_csv_file(
        ["position", "performance", "Level"],
        [["Backend Developer", "4.8", "Senior"], ["QA Engineer", "4.5", "Junior"]],
    )
    table = analysis_of_developer_performance(
        [file], keys=["position", "performance", "Level"]
    )
    assert table.get_rows() == [
        ["position", "performance", "Level"],
        ["Backend Developer", 4.8, "Senior"],
        ["QA Engineer", 4.5, "Junior"],
    ]


def test_analysis_without_keys():
    file = create_csv_file(
        ["position", "performance"],
        [["Backend Developer", "4.8"]],
    )
    table = analysis_of_developer_performance([file])  # keys=None
    assert table.get_rows() == [
        ["position", "performance"],
        ["Backend Developer", 4.8],
    ]

def test_analysis_mixed_values():
    file = create_csv_file(
        ["position", "performance"],
        [
            ["Backend Developer", "4"],
            ["QA Engineer", "4.6"],
            ["Java Developer", "N/A"]
        ],
    )
    table = analysis_of_developer_performance([file], keys=["position", "performance"])
    print("\n",table)
    # ожидаем, что значения сохранятся как есть (список)
    assert table.get_rows() == [
        ["position", "performance"],
        ["Backend Developer", 4.0],
        ["QA Engineer", 4.6],
        ["Java Developer", "N/A"]
    ]
