import pytest
from table import Table


@pytest.mark.parametrize(
    "columns,expected",
    [
        (["Position", "Performance"], [["Position", []], ["Performance", []]]),
        (["Name"], [["Name", []]]),
    ],
)
def test_create_matrix(columns, expected):
    table = Table(columns)
    assert table.matrix == expected


@pytest.mark.parametrize(
    "row,expected",
    [
        (
            ["Backend Developer", 4.8],
            [["Position", ["Backend Developer"]], ["Performance", [[4.8]]]],
        ),
        (
            ["QA Engineer", 4.5],
            [["Position", ["QA Engineer"]], ["Performance", [[4.5]]]],
        ),
    ],
)
def test_add_row_new_key(row, expected):
    table = Table(["Position", "Performance"])
    table.add_row(row)
    assert table.matrix == expected


def test_add_row_existing_key():
    table = Table(["Position", "Performance"])
    table.add_row(["Backend Developer", 4.8])
    table.add_row(["Backend Developer", 4.9])
    assert table.matrix == [
        ["Position", ["Backend Developer"]],
        ["Performance", [[4.8, 4.9]]],
    ]


def test_add_row_invalid_length():
    table = Table(["Position", "Performance"])
    with pytest.raises(ValueError):
        table.add_row(["OnlyOneValue"])


def test_add_row_without_columns():
    table = Table()
    with pytest.raises(ValueError):
        table.add_row(["Backend Developer", 4.8])


@pytest.mark.parametrize(
    "name,values,expected",
    [
        (
            "Experience",
            [5, 6],
            [["Position", []], ["Performance", []], ["Experience", [5, 6]]],
        ),
        ("Level", None, [["Position", []], ["Performance", []], ["Level", []]]),
    ],
)
def test_add_column(name, values, expected):
    table = Table(["Position", "Performance"])
    table.add_column(name, values)
    assert table.matrix == expected


def test_get_rows():
    table = Table(["Position", "Performance"])
    table.add_row(["Backend Developer", 4.8])
    table.add_row(["QA Engineer", 4.5])
    rows = table.get_rows()
    assert rows == [
        ["Position", "Performance"],
        ("Backend Developer", [4.8]),
        ("QA Engineer", [4.5]),
    ]


# --- Дополнительные тесты для полного покрытия --- #


def test_add_row_multiple_columns():
    table = Table(["Position", "Performance", "Level"])
    table.add_row(["Backend Developer", 4.8, "Senior"])
    assert table.matrix == [
        ["Position", ["Backend Developer"]],
        ["Performance", [[4.8]]],
        ["Level", [["Senior"]]],
    ]


def test_get_rows_empty_table():
    table = Table(["Position", "Performance"])
    rows = table.get_rows()
    # только заголовки, без данных
    assert rows == [["Position", "Performance"]]


def test_add_column_without_values():
    table = Table(["Position"])
    table.add_column("Performance")
    assert table.matrix == [["Position", []], ["Performance", []]]
