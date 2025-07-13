from app.ui import common
from datetime import datetime
from prompt_toolkit import prompt
from app.finance_traker import FinanceTracker


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
