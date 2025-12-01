import pytest
from table import Table
from reports import Reports


@pytest.mark.parametrize(
    "rows,expected",
    [
        (
            [["Backend Developer", 4.8], ["Backend Developer", 4.9]],
            [["Position", ["Backend Developer"]], ["Performance", [4.85]]],
        ),
        (
            [["QA Engineer", 4.5], ["QA Engineer", 4.7]],
            [["Position", ["QA Engineer"]], ["Performance", [4.6]]],
        ),
    ],
)
def test_count_average(rows, expected):
    table = Table(["Position", "Performance"])
    for r in rows:
        table.add_row(r)

    Reports.count_average(table, "Performance")
    assert table.matrix == expected


def test_count_average_invalid_column():
    table = Table(["Position", "Performance"])
    table.add_row(["Backend Developer", 4.8])
    with pytest.raises(ValueError):
        Reports.count_average(table, "Salary")


@pytest.mark.parametrize(
    "rows,column,reverse,expected",
    [
        (
            [["Backend Developer", 4.8], ["QA Engineer", 4.5], ["Data Scientist", 4.9]],
            "Performance",
            True,
            [
                ["Position", ["Data Scientist", "Backend Developer", "QA Engineer"]],
                ["Performance", [[4.9], [4.8], [4.5]]],
            ],
        ),
        (
            [["Backend Developer", 4.8], ["QA Engineer", 4.5], ["Data Scientist", 4.9]],
            "Performance",
            False,
            [
                ["Position", ["QA Engineer", "Backend Developer", "Data Scientist"]],
                ["Performance", [[4.5], [4.8], [4.9]]],
            ],
        ),
    ],
)
def test_sort_by_column(rows, column, reverse, expected):
    table = Table(["Position", "Performance"])
    for r in rows:
        table.add_row(r)

    Reports.sort_by_column(table, column, reverse=reverse)
    assert table.matrix == expected


def test_sort_by_column_invalid_column():
    table = Table(["Position", "Performance"])
    table.add_row(["Backend Developer", 4.8])
    with pytest.raises(ValueError):
        Reports.sort_by_column(table, "Salary")
