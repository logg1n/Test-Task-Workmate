import pytest
from table import Table
from reports import Reports


@pytest.mark.parametrize(
    "rows,expected",
    [
        (
            [["Backend Developer", 4.8], ["Backend Developer", 4.9]],
            [["position", "performance"], ["Backend Developer", 4.85]],
        ),
        (
            [["QA Engineer", 4.5], ["QA Engineer", 4.7]],
            [["position", "performance"], ["QA Engineer", 4.6]],
        ),
    ],
)
def test_count_average(rows, expected):
    table = Table(["position", "performance"])
    for r in rows:
        table.add_row(r)

    Reports.count_average(table, "performance")
    assert table.get_rows() == expected


def test_count_average_invalid_column():
    table = Table(["position", "performance"])
    table.add_row(["Backend Developer", 4.8])
    table.add_row(["QA Engineer", 4.5])

    with pytest.raises(ValueError):
        Reports.count_average(table, "Salary")


@pytest.mark.parametrize(
    "rows,reverse,expected",
    [
        (
            [["Backend Developer", 4.8], ["QA Engineer", 4.5], ["Data Scientist", 4.9]],
            True,
            [
                ["position", "performance"],
                ["Data Scientist", 4.9],
                ["Backend Developer", 4.8],
                ["QA Engineer", 4.5],
            ],
        ),
        (
            [["Backend Developer", 4.8], ["QA Engineer", 4.5], ["Data Scientist", 4.9]],
            False,
            [
                ["position", "performance"],
                ["QA Engineer", 4.5],
                ["Backend Developer", 4.8],
                ["Data Scientist", 4.9],
            ],
        ),
    ],
)
def test_sort_by_column(rows, reverse, expected):
    table = Table(["position", "performance"])
    for r in rows:
        table.add_row(r)

    Reports.sort_by_column(table, "performance", reverse=reverse)
    assert table.get_rows() == expected


def test_sort_by_column_invalid_column():
    table = Table(["position", "performance"])
    table.add_row(["Backend Developer", 4.8])
    table.add_row(["QA Engineer", 4.5])

    with pytest.raises(ValueError):
        Reports.sort_by_column(table, "Salary")


def test_count_average_non_numeric():
    table = Table(["position", "performance"])
    table.add_row(["Backend Developer", "N/A"])

    result = Reports.count_average(table, "performance")
    # Проверяем, что строка без чисел не ломает логику
    assert result.get_rows() == [["position", "performance"]]


def test_count_by_skill():
    table = Table(["skills"])
    table.add_row(["Python, Java"])
    table.add_row(["Python, SQL"])

    Reports.count_by_skill(table, "skills")
    assert table.get_rows() == [
        ["skills"],
        ["Python", 2],
        ["Java", 1],
        ["SQL", 1],
    ]


def test_count_by_skill_empty():
    table = Table(["skills"])
    table.add_row([""])
    Reports.count_by_skill(table, "skills")
    assert table.get_rows() == [["skills"]]
