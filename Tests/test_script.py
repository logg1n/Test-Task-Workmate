import pytest
import tempfile
import csv
from script import analysis_of_developer_performance


def create_csv_file(headers, rows):
    tmp = tempfile.NamedTemporaryFile(
        mode="w+", newline="", delete=False, encoding="utf-8"
    )
    writer = csv.writer(tmp)
    writer.writerow(headers)
    writer.writerows(rows)
    tmp.flush()
    return tmp.name


def test_analysis_basic():
    file = create_csv_file(
        ["Position", "Performance"],
        [["Backend Developer", "4.8"], ["QA Engineer", "4.5"]],
    )
    table = analysis_of_developer_performance([file], keys=["Position", "Performance"])
    assert table.get_rows() == [
        ["Position", "Performance"],
        ("Backend Developer", [4.8]),
        ("QA Engineer", [4.5]),
    ]


def test_analysis_no_keys():
    file = create_csv_file(["Position", "Performance"], [["Backend Developer", "4.8"]])
    table = analysis_of_developer_performance([file], keys=["Salary"])
    assert table.matrix == []


def test_analysis_multiple_files():
    file1 = create_csv_file(["Position", "Performance"], [["Backend Developer", "4.8"]])
    file2 = create_csv_file(["Position", "Performance"], [["QA Engineer", "4.5"]])
    table = analysis_of_developer_performance(
        [file1, file2], keys=["Position", "Performance"]
    )
    rows = table.get_rows()
    assert len(rows) == 3  # заголовки + 2 строки


def test_analysis_empty_files():
    table = analysis_of_developer_performance([], keys=["Position", "Performance"])
    assert table is None
