import os
from app.ui import common
from app.finance_traker import FinanceTracker, ensure_files_directory_exists
from app.transaction import Transaction
from prompt_toolkit import prompt
from app.validation import AmountValidator, DateValidator, type_completer
from datetime import datetime
from typing import Optional


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


def delete_transaction_ui(tracker: FinanceTracker) -> None:
    """Интерфейс для удаления транзакции."""
    common.display_header("Удаление транзакции")
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
        elif not filename.endswith(".csv"):
            filename += ".csv"

        tracker.delete_transaction(index, filename)
        print("✅ Транзакция успешно удалена!")
    except KeyboardInterrupt:
        print("\n⏹ Отменено пользователем.")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")


def show_balance_ui(tracker: FinanceTracker):
    """Функция для показа текущего баланса."""
    common.display_header("Текущий баланс")
    balance = tracker.get_balance()
    print(f"\n💵 Ваш текущий баланс: {balance:.2f} руб.")


def show_monthly_report_ui(tracker: FinanceTracker) -> None:
    """Функция для показа отчета за месяц."""
    common.display_header("Отчета за месяц")
    try:
        current_year = datetime.now().year
        year = int(prompt(f"Введите год (по умолчанию {current_year}): ") or current_year)
        month = int(prompt("Введите месяц (1-12): "))

        if month < 1 or month > 12:
            print("❌ Ошибка: Месяц должен быть от 1 до 12.")
            return
        report = tracker.get_monthly_report(month, year)
        if report:
            print(f"\n📊 Отчет за {month:02d}/{year}:")
            print("-" * 70)
            print(f"{'Дата':<12} | {'Тип':<8} | {'Категория':<20} | {'Сумма':>10}")
            print("-" * 70)
            for t in report:
                print(f"{t.date} | {t.type:<8} | {t.category:<20} | {t.amount:>10.2f} руб.")
            print("-" * 70)

            # Вывод итогов
            income = sum(t.amount for t in report if t.type == "income")
            expense = sum(t.amount for t in report if t.type == "expense")
            print(f"\nИтого доходов: {income:.2f} руб.")
            print(f"Итого расходов: {expense:.2f} руб.")
            print(f"Баланс за период: {(income - expense):.2f} руб.")
        else:
            print("Нет транзакций за указанный период.")
    except ValueError:
        print("❌ Ошибка: Введите корректные числовые значения.")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")


def plot_spending_ui(tracker: FinanceTracker) -> None:
    """Функция для визуализации расходов по категориям."""
    common.display_header("Анализ расходов")
    try:
        tracker.plot_spending_by_category()
        print("\n📈 График успешно построен!")
    except Exception as e:
        print(f"❌ Ошибка при построении графика: {e}")


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


def main_menu() -> None:
    """Главное меню программы."""
    common.clean_screen()
    tracker = FinanceTracker()

    # Загрузка данных
    selected_file = select_csv_file()
    if selected_file:
        tracker.load_from_csv(selected_file)
        print(f"\n✅ Данные успешно загружены из {selected_file}")
    else:
        print("\nРаботаем с новым файлом данных.")

    input("\nНажмите Enter для продолжения...")

    while True:
        common.clean_screen()
        common.display_header("Личный финансовый трекер")
        print("\nДоступные действия:")
        print("1. 📝 Добавить транзакцию")
        print("2. 💰 Показать баланс")
        print("3. 📅 Показать отчет за месяц")
        print("4. 📊 Визуализировать расходы")
        print("5. 💾 Экспорт в CSV")
        print("6. ✏️ Редактировать транзакцию")
        print("7. ❌ Удалить транзакцию")
        print("8. 🚪 Выйти")

        choice = prompt("\nВыберите действие (1-8): ").strip()

        if choice == "1":
            common.clean_screen()
            add_transaction_ui(tracker)
        elif choice == "2":
            common.clean_screen()
            show_balance_ui(tracker)
        elif choice == "3":
            common.clean_screen()
            show_monthly_report_ui(tracker)
        elif choice == "4":
            common.clean_screen()
            plot_spending_ui(tracker)
        elif choice == "5":
            common.clean_screen()
            export_to_csv_ui(tracker)
        elif choice == "6":
            common.clean_screen()
            edit_transaction_ui(tracker)
        elif choice == "7":
            common.clean_screen()
            delete_transaction_ui(tracker)
        elif choice == "8":
            print("\nДо свидания! 👋")
            break
        else:
            print("❌ Неверный выбор. Попробуйте снова.")
        
        input("\nНажмите Enter для продолжения...")
