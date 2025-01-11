from src.lang.messages import MSG_INCORRECT_INPUT

# Вынесено в отдельную функцию, потому что DRY,
# но на полноценный def не тянет. Сделано для демонстрации, что так тоже можно.
# Не соответствует PEP8
prompt_changer = lambda x: " (пустая строка для отмены): " if x else ": "


def show_menu(title: str, choices: dict[int, str], prompt: str = "Выберите действие",
              empty_allowed: bool = False) -> int | None:
    """Выводит меню с возможными вариантами выбора и ожидает ввода пользователем номера пункта меню.
    :param title: Заголовок меню
    :param choices: Словарь с вариантами выбора
    :param prompt: Текст подсказки ввода
    :param empty_allowed: Разрешить пустой ввод
    :return: Выбранный пункт меню или None, если пустой ввод разрешен
    """
    if choices is None or len(choices) == 0:
        return None

    if title is not None:
        print("\n", title)
    for key, choice in choices.items():
        print(f' {key:2}. {choice}')
    while True:
        try:
            user_input = input(prompt + prompt_changer(empty_allowed)).strip()
            if user_input == "" and empty_allowed:
                break
            user_input = int(user_input)
            if user_input in choices:
                return user_input
            else:
                print(MSG_INCORRECT_INPUT)
        except ValueError:
            print(MSG_INCORRECT_INPUT)
    return None


def show_table(title: str, rows: list[list[str]], headers: list[str] = None, sizes: list[int] = None) -> None:
    """Выводит таблицу
    :param title: Заголовок таблицы
    :param rows: Список строк таблицы
    :param headers: Список заголовков столбцов таблицы
    :param sizes: Список размеров столбцов таблицы, если не указаны, рассчитываются на основании rows и headers
    """
    def print_horizontal_line():
        print("+" + "+".join(["-" * size for size in sizes]) + "+")

    if rows is None or len(rows) == 0:
        return

    if title is not None:
        print("\n", title)

    if sizes is None:
        sizes = [0] * len(rows[0])
        for row in rows:
            for i, cell in enumerate(row):
                sizes[i] = max(sizes[i], len(cell))

    if headers is not None:
        for i, cell in enumerate(headers):
            sizes[i] = max(sizes[i], len(cell))
        print_horizontal_line()
        print("|" + "|".join([cell.center(size) for cell, size in zip(headers, sizes)]) + "|")

    print_horizontal_line()
    for row in rows:
        print("|" + "|".join([f"{cell:{size}}" for cell, size in zip(row, sizes)]) + "|")
    print_horizontal_line()


def input_string(prompt: str, empty_allowed: bool = False) -> str | None:
    """Вводит строку
    :param prompt: Строка подсказки
    :param empty_allowed: Если True, то пустая строка будет считаться корректным вводом, будет возвращено None
    :return: Введенная строка или None
    """
    while True:
        user_input = input(prompt + prompt_changer(empty_allowed)).strip()
        if user_input == "" and empty_allowed:
            break
        if len(user_input) > 0:
            return user_input
        else:
            print(MSG_INCORRECT_INPUT)
    # print("Отмена")
    return None


def input_int(prompt: str, min_value: int = None, max_value: int = None, empty_allowed: bool = False) -> int | None:
    """Вводит целое число
    :param prompt: Строка подсказки
    :param min_value: Минимальное значение, может быть опущено
    :param max_value: Максимальное значение, может быть опущено
    :param empty_allowed: Если True, то пустая строка будет считаться корректным вводом, будет возвращено None
    :return: Введенное число или None
    """

    if min_value is not None and max_value is not None and min_value > max_value:
        raise ValueError("min_value больше max_value")
    while True:
        try:
            user_input = input(prompt + prompt_changer(empty_allowed)).strip()
            if user_input == "" and empty_allowed:
                break
            user_input = int(user_input)
            if min_value is not None and user_input < min_value:
                print("Введенное значение меньше минимального")
            elif max_value is not None and user_input > max_value:
                print("Введенное значение больше максимального")
            else:
                return user_input
        except ValueError:
            print(MSG_INCORRECT_INPUT)
    # print("Отмена")
    return None


def print_info(info_type: str | None, message: str | None, pause: bool = False) -> None:
    """Выводит сообщение в консоль. Если указан тип выводимой информации, выводит его перед
    сообщением в квадратных скобках. Если параметр pause принимает значение True, то после вывода сообщения
    ожидается нажатие Enter
    Также может использоваться для остановки до нажатия Enter, если параметр message имеет значение None

    :param info_type: Тип выводимой информации, может быть None. Предполагаемые значения: "ОШИБКА", "ИНФОРМАЦИЯ"
    :param message: Выводимое сообщение
    :param pause: Указывает, нужно ли ожидать нажатие Enter после вывода сообщения
    """
    if message is not None:
        if info_type is not None:
            print(f"[{info_type}]", end=" ")
        print(message)
    if pause:
        input("   Нажмите Enter для продолжения")
