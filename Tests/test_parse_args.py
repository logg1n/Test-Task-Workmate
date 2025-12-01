import sys

import pytest

from run import get_args_command_line
from run import main


@pytest.mark.parametrize(
    "argv, expected_files, expected_reports",
    [
        (
            ["run.py", "--files", "file1.csv", "file2.csv", "--reports", "performance"],
            ["file1.csv", "file2.csv"],
            "performance",
        ),
        (
            ["run.py", "--files", "data.csv", "--reports", "performance"],
            ["data.csv"],
            "performance",
        ),
        (
            ["run.py", "--files", "data.csv", "--reports", "performance"],
            ["data.csv"],
            "performance",
        ),
        (
            ["run.py", "--files", "data.csv", "--reports", "performance"],
            ["data.csv"],
            "performance",
        ),
    ],
)
def test_get_args_command_line(monkeypatch, argv, expected_files, expected_reports):
    monkeypatch.setattr(sys, "argv", argv)
    files, reports = get_args_command_line()
    assert files == expected_files
    assert reports == expected_reports


def test_missing_files(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["run.py", "--reports", "performance"])
    with pytest.raises(SystemExit):
        get_args_command_line()


def test_unknown_argument(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["run.py", "--wrong"])

    with pytest.raises(SystemExit):
        get_args_command_line()


def test_reports_before_files(monkeypatch):
    # аргументы в другом порядке
    argv = ["run.py", "--reports", "performance", "--files", "data.csv"]
    monkeypatch.setattr(sys, "argv", argv)

    files, reports = get_args_command_line()
    assert files == ["data.csv"]
    assert reports == "performance"


def test_run_main(monkeypatch, tmp_path):
    file = tmp_path / "employees1.csv"
    file.write_text("position,performance\nBackend Developer,4.8\n")
    monkeypatch.setattr(
        sys, "argv", ["run.py", "--files", str(file), "--reports", "performance"]
    )
    main()
