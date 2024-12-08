from json import JSONDecodeError

from src.models.book import Book, book_statuses
from src.models.library import Library, CompatibilityError
from src.utils.interface import show_menu, input_string, input_int, print_info, show_table

LIBRARY_FILENAME = '../library.json'


def add_book_to_library(library: Library) -> None:
    """Добавление книги в библиотеку. Данные вводятся пользователем построчно - название, автор, год издания.
    Пустая строка прерывает процесс ввода.
    :param library: Библиотека
    :return: None
    :raises: ValueError
    """
    if library is None or not isinstance(library, Library):
        raise TypeError("Не передана библиотека")
    # Ожидаем ввода пользователя
    title = input_string('Введите название книги', True)
    if title is None:
        print_info("ИНФОРМАЦИЯ", "Добавление книги отменено")
        return
    # Ожидаем ввода пользователя
    author = input_string('Введите автора книги', True)
    if author is None:
        print_info("ИНФОРМАЦИЯ", "Добавление книги отменено")
        return
    # Ожидаем ввода пользователя
    # В 1457 году была издана первая книга с установленной датой
    year = input_int("Введите год издания книги не ранее 1457", min_value=1457, empty_allowed=True)
    if year is None:
        print_info("ИНФОРМАЦИЯ", "Добавление книги отменено")
        return
    library.add_book(Book(title, author, year))
    print_info("ИНФОРМАЦИЯ", "Книга добавлена")


def remove_book_from_library(library: Library) -> None:
    """Удаление книги из библиотеки. ID книги вводится пользователем.
    Пустая строка прерывает процесс удаления.
    :param library:
    :return: None
    :raises: ValueError
    """
    if library is None or not isinstance(library, Library):
        raise TypeError("Не передана библиотека")
    # Ожидаем ввода пользователя
    book_id = input_int("Введите id книги для удаления", empty_allowed=True)
    if book_id is None:
        print_info("ИНФОРМАЦИЯ", "Удаление книги отменено")
        return
    try:
        library.remove_book(book_id)
        print_info("ИНФОРМАЦИЯ", "Книга удалена")
    except KeyError:
        print_info("ОШИБКА", "Книга с таким id не найдена", True)


def find_books_by_title(library: Library) -> None:
    """Поиск книг по названию.
    :param library:
    :return: None
    :raises: ValueError
    """
    if library is None or not isinstance(library, Library):
        raise TypeError("Не передана библиотека")
    # Ожидаем ввода пользователя
    pattern = input_string("Введите подстроку для поиска по названию книги", True)
    if pattern is None:
        print_info("ИНФОРМАЦИЯ", "Поиск отменен")
        return
    books = library.find_books_by_title(pattern)
    if len(books) == 0:
        print_info("ИНФОРМАЦИЯ", "Книг c подходящим названием не найдено",True)
        return
    show_books(f"Найдено {len(books)} книг", books)


def find_books_by_author(library: Library) -> None:
    """Поиск книг по автору.
    :param library:
    :return: None
    :raises: ValueError
    """
    if library is None or not isinstance(library, Library):
        raise TypeError("Не передана библиотека")
    # Ожидаем ввода пользователя
    pattern = input_string("Введите подстроку для поиска по автору книги", True)
    if pattern is None:
        print_info("ИНФОРМАЦИЯ", "Поиск отменен")
        return
    books = library.find_books_by_author(pattern)
    if len(books) == 0:
        print_info("ИНФОРМАЦИЯ", "Книг c подходящим автором не найдено",True)
        return
    show_books(f"Найдено {len(books)} книг", books)


def find_books_by_year(library: Library) -> None:
    """Поиск книг по году издания.
    :param library:
    :return: None
    :raises: ValueError
    """
    if library is None or not isinstance(library, Library):
        raise TypeError("Не передана библиотека")
    # Ожидаем ввода пользователя
    year = input_int("Введите год издания книги", empty_allowed=True)
    if year is None:
        print_info("ИНФОРМАЦИЯ", "Поиск отменен")
        return
    books = library.find_books_by_year(year)
    if len(books) == 0:
        print_info("ИНФОРМАЦИЯ", "Книг c указанным годом издания не найдено",True)
        return
    show_books(f"Найдено {len(books)} книг", books)


def find_books_by_status(library: Library) -> None:
    """Поиск книг по статусу.
    :param library:
    :return: None
    :raises: ValueError
    """
    if library is None or not isinstance(library, Library):
        raise TypeError("Не передана библиотека")
    # Выводим перечень возможных статусов, ожидаем ввода пользователя
    status = show_menu("Укажите статус книги:",
                       {i: book_statuses[i] for i in range(1, len(book_statuses))},
                       prompt="Введите номер статуса", empty_allowed=True)
    # Пользователь отказался от выбора
    if status is None:
        print_info("ИНФОРМАЦИЯ", "Поиск отменен")
        return
    books = library.find_books_by_status(status)
    if len(books) == 0:
        print_info("ИНФОРМАЦИЯ", "Книг c указанным статусом не найдено",True)
        return
    show_books(f"Найдено {len(books)} книг", books)


def find_books(library: Library) -> None:
    """Поиск книг по названию, автору, году издания или статусу.
    :param library:
    :return: None
    :raises: ValueError
    """
    if library is None or not isinstance(library, Library):
        raise TypeError("Не передана библиотека")
    while True:
        # Выводим варианты поиска, ожидаем ввода пользователя
        n = show_menu("Поиск книг:",
                      {1: "По названию",
                       2: "По автору",
                       3: "По году издания",
                       4: "По статусу"}, empty_allowed=True)
        # Пользователь отказался от выбора
        if n is None:
            print_info("ИНФОРМАЦИЯ", "Поиск отменен")
            return
        if n == 1:
            find_books_by_title(library)
        elif n == 2:
            find_books_by_author(library)
        elif n == 3:
            find_books_by_year(library)
        elif n == 4:
            find_books_by_status(library)


def show_books(title: str, books: dict[int, Book]) -> None:
    """Вывод списка книг в табличном виде.
    :param title: Заголовок таблицы
    :param books: Словарь книг
    :return: None
    """
    if books is None or len(books) == 0:
        print_info("ИНФОРМАЦИЯ", "Книг не найдено", True)
        return

    table = []
    for book_id, book in books.items():
        table.append([f"{book_id:>3d}", book.title, book.author, str(book.year).center(11), book_statuses[book.status]])

    show_table(title, table, [" id ", "Название", "Автор", "Год издания", "Статус"])
    print_info(None, None, True)


def change_book_status(library: Library) -> None:
    """Изменение статуса книги. ID книги вводится пользователем. Статус выбирается пользователем по номеру
    из перечня доступных. Пустая строка прерывает процесс изменения статуса.
    :param library:
    :return: None
    :raises: ValueError
    """
    if library is None or not isinstance(library, Library):
        raise TypeError("Не передана библиотека")
    book_id = input_int("Введите id книги для изменения статуса", empty_allowed=True)
    if book_id is None:
        print_info("ИНФОРМАЦИЯ", "Изменение статуса книги отменено")
        return
    # Проверяем, есть ли такая книга в библиотеке. Если нет - выводим сообщение об ошибке и не просим ввести статус
    if book_id not in library.get_all_ids():
        print_info("ОШИБКА", "Книга с таким id не найдена", True)
        return
    # Выводим список доступных статусов, ожидаем ввода пользователя
    status = show_menu("Доступные статусы:",
                       {i: book_statuses[i] for i in range(1, len(book_statuses))},
                       prompt="Введите номер статуса", empty_allowed=True)
    # Пользователь отказался от выбора нового статуса - выходим
    if status is None:
        print_info("ИНФОРМАЦИЯ", "Изменение статуса книги отменено")
        return
    # Меняем статус
    try:
        library.change_book_status(book_id, status)
        print_info("ИНФОРМАЦИЯ", "Статус книги изменен")
    except KeyError:
        print_info("ОШИБКА", "Книга с таким id не найдена", True)


def main():
    """Главная функция программы"""
    print_info("ИНФОРМАЦИЯ", "Программа для работы с библиотекой книг")
    # Создаем библиотеку и загружаем данные из файла
    library = Library()
    try:
        with open(LIBRARY_FILENAME, 'r', encoding='utf-8') as f:
            library.load_from_json(f)
    except FileNotFoundError:
        # Файла нет - это нормально
        print_info("ИНФОРМАЦИЯ", f"Файл {LIBRARY_FILENAME} не найден, запуск считается первичным")
    except CompatibilityError as e:
        # Файл создан не в этой версии, работоспособность не гарантирована.
        # Язык сообщений - русский, так что можно выводить на экран
        print_info("ФАТАЛЬНАЯ ОШИБКА", str(e), True)
        exit(1)
    except JSONDecodeError:
        # Файл есть, но не может быть прочитан - дальше не работаем.
        # Выводим понятное сообщение
        print_info("ФАТАЛЬНАЯ ОШИБКА",
                   f"Ошибка при разборе содержимого файла {LIBRARY_FILENAME}", True)
        exit(1)
    else:
        print_info("ИНФОРМАЦИЯ", "Данные загружены")

    # Основной цикл программы
    while True:
        # Выводим меню и ожидаем реакции пользователя
        n = show_menu("-> Главное меню библиотеки <-",
                      {1: "Добавление книги",
                       2: "Удаление книги",
                       3: "Поиск книг...",
                       4: "Отображение всех книг",
                       5: "Изменение статуса книги",
                       0: "Выход"})
        # Пользователь что-то выбрал - исполняем
        if n == 1:
            add_book_to_library(library)
        elif n == 2:
            remove_book_from_library(library)
        elif n == 3:
            find_books(library)
        elif n == 4:
            show_books("Все книги нашей библиотеки", library.get_all_books())
        elif n == 5:
            change_book_status(library)
        elif n == 0:
            break
    # Выход из основного цикла, завершаем работу
    # Если библиотека изменена - сохраняем
    if library.get_changed():
        try:
            with open(LIBRARY_FILENAME, 'w', encoding='utf-8') as f:
                library.save_to_json(f)
            print_info("ИНФОРМАЦИЯ", "Данные сохранены")
        except Exception as e:
            print_info("ФАТАЛЬНАЯ ОШИБКА", str(e), True)
            exit(1)
    else:
        print_info("ИНФОРМАЦИЯ", "Данные не изменены, сохранение не требуется")


if __name__ == '__main__':
    main()
