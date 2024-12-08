book_statuses = [
    "",
    "в наличии",
    "выдана"
]


class Book(object):
    """Класс, описывающий книгу. Имеет поля и соответствующие методы `get_`
    :param title: название книги
    :param author: автор книги
    :param year: год издания
    :param status: статус книги (число в пределах элементов списка `book_statuses`)

    Метод `set_status()` устанавливает статус книги (число в пределах элементов списка `book_statuses`)
    """
    def __init__(self, title: str, author: str, year: int, status: int = 1) -> None:

        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def get_title(self) -> str:
        """Возвращает название книги"""
        return self.title

    def get_author(self) -> str:
        """Возвращает автора книги"""
        return self.author

    def get_year(self) -> int:
        """Возвращает год издания"""
        return self.year

    def get_status(self) -> int:
        """Возвращает статус книги (число в пределах элементов списка `book_statuses`)"""
        return self.status

    def set_status(self, status: int) -> None:
        """Устанавливает статус книги (число в пределах элементов списка `book_statuses`)"""
        if not isinstance(status, int):
            raise TypeError("Статус книги должен быть числом")
        if status not in range(len(book_statuses)):
            raise ValueError("Неверный статус книги")
        self.status = status

    def to_dict(self) -> dict:
        """Возвращает книгу в виде словаря для экспорта в json"""
        return self.__dict__
