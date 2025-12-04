import sys
import pytest
import coverage

if __name__ == "__main__":
    # Инициализируем coverage
    cov = coverage.Coverage(
        source=["."]
    )
    cov.start()

    # Запускаем pytest на каталог Tests
    exit_code = pytest.main(["-q", "./"])

    # Останавливаем coverage и сохраняем данные
    cov.stop()
    cov.save()

    # Выводим отчёт в консоль
    cov.report(show_missing=True)

    # Можно также сохранить HTML‑отчёт
    cov.html_report(directory="htmlcov")

    sys.exit(exit_code)
