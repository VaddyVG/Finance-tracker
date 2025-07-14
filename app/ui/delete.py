from app.finance_traker import FinanceTracker
from app.ui import common
from prompt_toolkit import prompt


def delete_transaction_ui(tracker: FinanceTracker) -> None:
    """Интерфейс для удаления транзакции."""
    common.display_header("Удаление транзакции")
    try:
        if not tracker.transactions:
            print("Нет транзакций для удаления.")
            return

        print("\nСписок транзакций:")
        for i, t in enumerate(tracker.transactions, 1):
            print(f"{i}. {t}")

        index = int(prompt("\nВведите индекс транзакции для удаления: "))
        if not (0 <= index <= len(tracker.transactions)):
            print("❌ Неверный индекс транзакции.")
            return

        filename = prompt("Введите имя файла для сохранения (например, data.csv): ").strip()
        if not filename:
            print("❌ Ошибка: Имя файла не может быть пустым.")
            return
        elif not filename.endswith(".csv"):
            filename += ".csv"

        tracker.delete_transaction(index, filename)
        print("✅ Транзакция успешно удалена!")
    except KeyboardInterrupt:
        print("\n⏹ Отменено пользователем.")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
