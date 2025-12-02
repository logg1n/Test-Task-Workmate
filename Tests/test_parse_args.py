import sys
import pytest

from run import get_args_command_line, main


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
            ["run.py", "--reports", "performance", "--files", "data.csv"],
            ["data.csv"],
            "performance",
        ),
    ],
)
def test_get_args_command_line(monkeypatch, argv, expected_files, expected_reports):
    """Проверяем корректный парсинг аргументов CLI"""
    monkeypatch.setattr(sys, "argv", argv)
    files, reports = get_args_command_line()
    assert files == expected_files
    assert reports == expected_reports


def test_missing_files(monkeypatch):
    """Если не указаны --files → SystemExit"""
    monkeypatch.setattr(sys, "argv", ["run.py", "--reports", "performance"])
    with pytest.raises(SystemExit):
        get_args_command_line()


def test_unknown_argument(monkeypatch):
    """Неизвестный аргумент → SystemExit"""
    monkeypatch.setattr(sys, "argv", ["run.py", "--wrong"])
    with pytest.raises(SystemExit):
        get_args_command_line()


def test_run_main(monkeypatch, tmp_path, capsys):
    """Проверяем полный запуск main() с тестовым CSV"""
    file = tmp_path / "employees1.csv"
    file.write_text("position,performance\nBackend Developer,4.8\n")

    monkeypatch.setattr(
        sys, "argv", ["run.py", "--files", str(file), "--reports", "performance"]
    )

    main()
    captured = capsys.readouterr()

    # Проверяем, что в выводе есть заголовки и данные
    assert "position" in captured.out
    assert "performance" in captured.out
    assert "Backend Developer" in captured.out
    assert "4.80" in captured.out
