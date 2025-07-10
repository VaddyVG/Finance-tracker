import os


def display_header(title: str) -> None:
    """Отображает заголовок с рамкой."""
    print("\n" + "=" * 50)
    print(f"{title:^50}")
    print("=" * 50)


def clean_screen() -> None:
    """Очищает экран консоли."""
    os.system("cls" if os.name == "nt" else "clear")