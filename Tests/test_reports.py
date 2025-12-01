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


@pytest.mark.parametrize(
    "rows,column",
    [
        ([["Backend Developer", 4.8], ["QA Engineer", 4.5]], "Salary"),
    ],
)
def test_count_average_invalid_column(rows, column):
    table = Table(["Position", "Performance"])
    for r in rows:
        table.add_row(r)

    with pytest.raises(ValueError, match="Колонка 'Salary' не найдена"):
        Reports.count_average(table, column)


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


@pytest.mark.parametrize(
    "rows,column",
    [
        ([["Backend Developer", 4.8], ["QA Engineer", 4.5]], "Salary"),
    ],
)
def test_sort_by_column_invalid_column(rows, column):
    table = Table(["Position", "Performance"])
    for r in rows:
        table.add_row(r)

    with pytest.raises(ValueError, match="Колонка 'Salary' не найдена"):
        Reports.sort_by_column(table, column)


@pytest.mark.parametrize(
    "rows,expected",
    [
        ([["Backend Developer", "N/A"]], []),
    ],
)
def test_count_average_non_numeric(rows, expected):
    table = Table(["Position", "Performance"])
    for r in rows:
        table.add_row(r)

    result = Reports.count_average(table, "Performance")
    # Проверяем, что строка без чисел не ломает логику
    assert result.matrix[1][1] == expected
