"""HW3: загружает данные, предлагает выбрать задачу.

Использование:
    python main.py                 —  выбор задачи
    python main.py overview        —  2: информация о наборе данных
    python main.py survival        —  3: выживаемость по классам
    python main.py names           —  4: популярные имена
    python main.py names-by-class  —  5: популярные имена по классам
    python main.py older           —  6: пассажиры старше 44 лет
    python main.py younger-males   —  7: мужчины младше 44 лет
    python main.py cabins          —  8: количество n-местных кают
"""

import sys

from titanic import cabins, filters, loader, names, overview, survival

# Реестр задач: имя команды -> (описание, функция, принимающая DataFrame)
TASKS = {
    "overview": ("Информация о наборе данных", overview.run),
    "survival": ("Выживаемость по классам", survival.run),
    "names": ("Популярные имена", names.run),
    "names-by-class": ("Популярные имена по классам", names.run_by_class),
    "older": ("Пассажиры старше 44 лет", filters.run),
    "younger-males": ("Мужчины младше 44 лет", filters.run_younger_males),
    "cabins": ("Количество n-местных кают", cabins.run),
}


def ask_task() -> str | None:
    """Показывает диалог выбора задачи и возвращает имя команды или None."""
    keys = list(TASKS)
    print("Доступные задачи:")
    for i, key in enumerate(keys, start=1):
        description = TASKS[key][0]
        print(f"  {i}. {key:<15} — {description}")

    while True:
        try:
            raw = input("\nВведите номер или имя задачи (q — выход): ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return None

        if raw.lower() in {"q", "quit", "exit"}:
            return None

        # Ввод номера
        if raw.isdigit():
            idx = int(raw)
            if 1 <= idx <= len(keys):
                return keys[idx - 1]
            print(f"Нет задачи с номером {idx}. Попробуйте снова.")
            continue

        # Ввод имени
        if raw in TASKS:
            return raw

        print(f"Неизвестная задача: {raw!r}. Попробуйте снова.")


def main(argv: list[str]) -> int:
    if argv:
        task = argv[0]
        if task not in TASKS:
            print(f"Неизвестная задача: {task!r}\n")
            task = ask_task()
    else:
        task = ask_task()

    if task is None:
        print("Выход.")
        return 1

    df = loader.load()
    TASKS[task][1](df)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))