from app.finance_traker import FinanceTracker
from prompt_toolkit import prompt
from app.ui import (
    common, show_results, add_and_edit, work_csv, delete)


def main_menu() -> None:
    """Главное меню программы."""
    common.clean_screen()
    tracker = FinanceTracker()

    # Загрузка данных
    selected_file = work_csv.select_csv_file()
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
            add_and_edit.add_transaction_ui(tracker)
        elif choice == "2":
            common.clean_screen()
            show_results.show_balance_ui(tracker)
        elif choice == "3":
            common.clean_screen()
            show_results.show_monthly_report_ui(tracker)
        elif choice == "4":
            common.clean_screen()
            show_results.plot_spending_ui(tracker)
        elif choice == "5":
            common.clean_screen()
            work_csv.export_to_csv_ui(tracker)
        elif choice == "6":
            common.clean_screen()
            add_and_edit.edit_transaction_ui(tracker)
        elif choice == "7":
            common.clean_screen()
            delete.delete_transaction_ui(tracker)
        elif choice == "8":
            print("\nДо свидания! 👋")
            break
        else:
            print("❌ Неверный выбор. Попробуйте снова.")
        
        input("\nНажмите Enter для продолжения...")


def main():
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nПрограмма завершена пользователем.")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
    finally:
        print("\nСпасибо за использование финансового трекера!")
