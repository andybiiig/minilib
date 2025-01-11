import json
from typing import TextIO

from src.lang.messages import ERR_LIBRARY_FILE_INVALID, ERR_ONLY_BOOKS_ALLOWED
from src.models.book import Book

LIBRARY_VERSION = '0.1'


class CompatibilityError(Exception):
    pass


class Library(object):
    def __init__(self):
        self.version = LIBRARY_VERSION
        self.books = {}
        self.next_id = 1
        self.changed = False

    def get_changed(self) -> bool:
        return self.changed

    def add_book(self, book: Book) -> None:
        if not isinstance(book, Book):
            raise TypeError(ERR_ONLY_BOOKS_ALLOWED)

        self.books[self.next_id] = book
        self.next_id += 1
        self.changed = True

    def remove_book(self, book_id: int) -> None:
        del self.books[book_id]
        self.changed = True

    def get_book(self, book_id: int) -> Book:
        return self.books[book_id]

    def change_book_status(self, book_id: int, status: int) -> None:
        current_status = self.books[book_id].get_status()
        if current_status == status:
            return
        self.books[book_id].set_status(status)
        self.changed = True

    def get_all_ids(self) -> list[int]:
        return list(self.books.keys())

    def get_all_books(self) -> dict[int, Book]:
        return self.books

    def find_books_by_author(self, author: str) -> dict[int, Book]:
        author = author.lower()
        return {x: self.books[x] for x in self.books if author in self.books[x].get_author().lower()}

    def find_books_by_title(self, title: str) -> dict[int, Book]:
        title = title.lower()
        return {x: self.books[x] for x in self.books if title in self.books[x].get_title().lower()}

    def find_books_by_year(self, year: int) -> dict[int, Book]:
        return {x: self.books[x] for x in self.books if year == self.books[x].get_year()}

    def find_books_by_status(self, status: int) -> dict[int, Book]:
        return {x: self.books[x] for x in self.books if status == self.books[x].get_status()}

    def load_from_json(self, file: TextIO) -> None:
        self.books = {}
        self.next_id = 1
        library_data = json.load(file)
        if 'lib_version' not in library_data:
            raise TypeError(ERR_LIBRARY_FILE_INVALID)

        if library_data['lib_version'] != self.version:
            raise CompatibilityError(f"Версия библиотеки {library_data['lib_version']} не поддерживается")

        if 'books' not in library_data:
            raise TypeError(ERR_LIBRARY_FILE_INVALID)

        for key, value in library_data['books'].items():
            key = int(key)
            self.books[key] = Book(value['title'],
                                   value['author'],
                                   value['year'],
                                   value['status'])
            if self.next_id <= key:
                self.next_id = key + 1
        self.changed = False

    def save_to_json(self, file: TextIO) -> None:
        json.dump({'lib_version': self.version,
                   'books': {x: self.books[x].to_dict() for x in self.books.keys()}}, file)
