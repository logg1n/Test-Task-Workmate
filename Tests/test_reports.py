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
def test_performance(rows, expected):
    table = Table(["position", "performance"])
    for r in rows:
        table.add_row(r)

    config = Reports.load_report("performance")
    for cb in config["callbacks"]:
        table = cb(table)

    assert table.get_rows() == expected


def test_performance_invalid_column():
    table = Table(["position", "performance"])
    table.add_row(["Backend Developer", 4.8])
    table.add_row(["QA Engineer", 4.5])

    config = Reports.load_report("performance")
    with pytest.raises(ValueError):
        config["callbacks"][0](table, "Salary")


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

    config = Reports.load_report("performance")
    # второй callback — сортировка
    table = config["callbacks"][1](table, "performance", reverse=reverse)

    assert table.get_rows() == expected


def test_sort_by_column_invalid_column():
    table = Table(["position", "performance"])
    table.add_row(["Backend Developer", 4.8])
    table.add_row(["QA Engineer", 4.5])

    config = Reports.load_report("performance")
    with pytest.raises(ValueError):
        config["callbacks"][1](table, "Salary")


def test_performance_non_numeric():
    table = Table(["position", "performance"])
    table.add_row(["Backend Developer", "N/A"])

    config = Reports.load_report("performance")
    table = config["callbacks"][0](table, "performance")

    # Проверяем, что некорректные значения игнорируются
    assert table.get_rows() == [["position", "performance"]]


def test_count_by_skill():
    table = Table(["skills"])
    table.add_row(["Python, Java"])
    table.add_row(["Python, SQL"])

    config = Reports.load_report("skills")
    table = config["callbacks"][0](table, "skills")

    # ✅ оставляем оригинальный заголовок "skills"
    assert table.get_rows() == [
        ["skills"],
        ["Python", 2],
        ["Java", 1],
        ["SQL", 1],
    ]


def test_count_by_skill_empty():
    table = Table(["skills"])
    table.add_row([""])

    config = Reports.load_report("skills")
    table = config["callbacks"][0](table, "skills")

    # ✅ таблица остаётся с тем же заголовком
    assert table.get_rows() == [["skills"]]
