from app.finance_traker import FinanceTracker
from app.transaction import Transaction
from prompt_toolkit import prompt
from app.validation import AmountValidator, DateValidator, type_completer
from app.ui import common


def add_transaction_ui(tracker: FinanceTracker) -> None:
    """Функция для добавления транзакции (взаимодействие с пользователем)."""
    common.display_header("Добавление транзакции")
    try:
        amount = prompt(("Введите сумму: "), validator=AmountValidator())
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
    common.display_header("Редактирование транзакции")
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
        elif not filename.endswith(".csv"):
            filename += ".csv"

        new_transaction = Transaction(amount, category, date, transaction_type)
        tracker.edit_transaction(index, new_transaction, filename)
        print("✅ Транзакция успешно отредактирована!")
    except KeyboardInterrupt:
        print("\n⏹ Отменено пользователем.")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
