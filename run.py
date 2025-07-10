from app.main import main_menu


def main():
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nПрограмма завершена пользователем.")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
    finally:
        print("\nСпасибо за использование финансового трекера!")


if __name__ == "__main__":
    main()
