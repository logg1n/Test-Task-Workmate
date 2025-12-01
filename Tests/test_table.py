import pytest
from table import Table


def test_create_table_with_columns():
    table = Table(["position", "performance"])
    assert table.get_rows() == [["position", "performance"]]


@pytest.mark.parametrize(
    "row,expected",
    [
        (
            ["Backend Developer", 4.8],
            [["position", "performance"], ["Backend Developer", 4.8]],
        ),
        (
            ["QA Engineer", 4.5],
            [["position", "performance"], ["QA Engineer", 4.5]],
        ),
    ],
)
def test_add_row(row, expected):
    table = Table(["position", "performance"])
    table.add_row(row)
    assert table.get_rows() == expected


def test_add_multiple_rows():
    table = Table(["position", "performance"])
    table.add_row(["Backend Developer", 4.8])
    table.add_row(["QA Engineer", 4.5])
    assert table.get_rows() == [
        ["position", "performance"],
        ["Backend Developer", 4.8],
        ["QA Engineer", 4.5],
    ]


def test_add_row_invalid_length():
    table = Table(["position", "performance"])
    with pytest.raises(ValueError):
        table.add_row(["OnlyOneValue"])


def test_get_rows_empty_table():
    table = Table(["position", "performance"])
    assert table.get_rows() == [["position", "performance"]]


def test_replace_table():
    table = Table(["position", "performance"])
    table.add_row(["Backend Developer", 4.8])

    # заменяем таблицу новыми заголовками и строками
    new_headers = ["Name", "Score"]
    new_rows = [["Alice", 5.0], ["Bob", 4.5]]
    table.replace(new_headers, new_rows)

    assert table.get_rows() == [
        ["Name", "Score"],
        ["Alice", 5.0],
        ["Bob", 4.5],
    ]
