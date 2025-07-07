import os
from app.finance_traker import FinanceTracker, ensure_files_directory_exists
from app.transaction import Transaction
from prompt_toolkit import prompt
from app.validation import AmountValidator, DateValidator, type_completer
from datetime import datetime
from typing import Optional


def display_header(title: str) -> None:
    """Отображает заголовок с рамкой."""
    print("\n" + "=" * 50)
    print(f"{title:^50}")
    print("=" * 50)


def clean_screen() -> None:
    """Очищает экран консоли."""
    os.system("cls" if os.name == "nt" else "clear")


def add_transaction_ui(tracker: FinanceTracker) -> None:
    """Функция для добавления транзакции (взаимодействие с пользователем)."""
    display_header("Добавление транзакции")
    try:
        amount = float(prompt("Введите сумму: "), validator=AmountValidator())
        category = prompt("Введите категорию: ").strip()
        if not category:
            print("❌ Ошибка: Категория не может быть пустой.")
            return

        date = prompt("Введите дату (ГГГГ-ММ-ДД): ", validator=DateValidator())
        transaction_type = prompt(
            "Введите тип (income/expense): ",
            completer=type_completer,
            complete_while_typing=True
        ).lower()

        if transaction_type not in ("income", "expense"):
            print("❌ Ошибка: Тип должен быть 'income' или 'expense'")
            return

        transaction = Transaction(amount, category, date, transaction_type)
        tracker.add_transaction(transaction)
        print("✅ Транзакция успешно добавлена!")
    except KeyboardInterrupt:
        print("\n⏹ Отменено пользователем.")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")


def edit_transaction_ui(tracker: FinanceTracker) -> None:
    """Интерфейс для редактирования транзакции."""
    display_header("Редактирование транзакции")
    try:
        if not tracker.transactions:
            print("Нет транзакций для редактирования.")
            return

        print("\nСписок транзакций:")
        for i, t in enumerate(tracker.transactions):
            print(f"{i}. {t}")

        index = int(prompt("\nВведите индекс транзакции для редактирования: "))
        if not (0 <= index < len(tracker.transactions)):
            print("❌ Неверный индекс транзакции.")
            return

        amount = float(prompt("Введите новую сумму: ", validator=AmountValidator()))
        category = prompt("Введите новую категорию: ").strip()
        if not category:
            print("❌ Ошибка: категория не может быть пустой.")
            return

        date = prompt("Введите новую дату (ГГГГ-ММ-ДД): ", validator=DateValidator())
        transaction_type = prompt(
            "Введите новый тип (income/expense): ",
            completer=type_completer,
            complete_while_typing=True
        ).lower()
        if transaction_type not in ("income", "expense"):
            print("❌ Ошибка: Тип должен быть 'income' или 'expense'")
            return

        filename = prompt("Введите имя файла для сохранения (например, data.csv): ").strip()
        if not filename:
            print("❌ Ошибка: Имя файла не может быть пустым.")
            return

        new_transaction = Transaction(amount, category, date, transaction_type)
        tracker.edit_transaction(index, new_transaction, filename)
        print("✅ Транзакция успешно отредактирована!")
    except KeyboardInterrupt:
        print("\n⏹ Отменено пользователем.")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")


def delete_transaction_ui(tracker: FinanceTracker) -> None:
    """Интерфейс для удаления транзакции."""
    display_header("Удаление транзакции")
    try:
        if not tracker.transactions:
            print("Нет транзакций для удаления.")
            return

        print("\nСписок транзакций:")
        for i, t in enumerate(tracker.transactions):
            print(f"{i}. {t}")

        index = int(prompt("\nВведите индекс транзакции для удаления: "))
        if not (0 <= index < len(tracker.transactions)):
            print("❌ Неверный индекс транзакции.")
            return

        filename = prompt("Введите имя файла для сохранения (например, data.csv): ").strip()
        if not filename:
            print("❌ Ошибка: Имя файла не может быть пустым.")
            return

        tracker.delete_transaction(index, filename)
        print("✅ Транзакция успешно удалена!")
    except KeyboardInterrupt:
        print("\n⏹ Отменено пользователем.")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")


def show_balance_ui(tracker: FinanceTracker):
    """Функция для показа текущего баланса."""
    display_header("Текущий баланс")
    balance = tracker.get_balance()
    print(f"\n💵 Ваш текущий баланс: {balance:.2f} руб.")


def plot_spending_ui(tracker: FinanceTracker) -> None:
    """Функция для визуализации расходов по категориям."""
    display_header("Анализ расходов")
    try:
        tracker.plot_spending_by_category()
        print("\n📈 График успешно построен!")
    except Exception as e:
        print(f"❌ Ошибка при построении графика: {e}")


def export_to_csv_ui(tracker: FinanceTracker):
    """Функция для экспорта данных в CSV."""
    display_header("Экспорт данных")
    try:
        default_filename = f"transactions_{datetime.now().strftime('%-Y%m-%d')}.csv"
        filename = prompt(f"Введите имя файла (по умолчанию {default_filename}): ").strip() or default_filename
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
