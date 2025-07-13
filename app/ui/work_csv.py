import os
from datetime import datetime
from app.finance_traker import FinanceTracker, ensure_files_directory_exists
from prompt_toolkit import prompt
from app.ui import common
from typing import Optional


def export_to_csv_ui(tracker: FinanceTracker):
    """Функция для экспорта данных в CSV."""
    common.display_header("Экспорт данных")
    try:
        default_filename = f"transactions_{datetime.now().strftime('%-Y%m-%d')}.csv"
        filename = prompt(f"Введите имя файла (по умолчанию {default_filename}): ").strip() or default_filename
        if not filename.endswith(".csv"):
            filename += ".csv"
        filepath = os.path.join("files", filename)
        if os.path.exists(filepath):
            choice = prompt("⚠️ Файл уже существует. Перезаписать? (y/n): ").strip().lower()
            if choice != "y":
                print("⏹ Экспорт отменен.")
                return

        tracker.export_to_csv(filename)
        print(f"✅ Данные успешно экспортированы в файл {filename}")
    except KeyboardInterrupt:
        print("\n⏹ Отменено пользователем.")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")


def select_csv_file() -> Optional[str]:
    """Показывает список CSV-файлов в директории files и позволяет выбрать один."""
    ensure_files_directory_exists()
    csv_files = [f for f in os.listdir("files") if f.endswith(".csv")]

    if not csv_files:
        print("CSV-файлы не найдены. Начните с пустого списка.")
        return None

    common.display_header("Выбор файла данных")
    print("\nДоступные CSV-файлы:")
    for i, filename in enumerate(csv_files, 1):
        print(f"{i}. {filename}")
    print(f"{len(csv_files)+1}. Создать новый файл")

    while True:
        choice = prompt("\nВыберите номер файла или действие: ").strip()
        if choice.isdigit():
            choice_num = int(choice)
            if 1 <= choice_num <= len(csv_files):
                return csv_files[choice_num - 1]
            elif choice_num == len(csv_files) + 1:
                return None
        print("❌ Неверный выбор. Попробуйте снова.")
