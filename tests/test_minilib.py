import io
import pytest
from mock import patch
from src.minilib import *


@pytest.fixture()
def json_file_wrapper():
    reader = io.StringIO('{"lib_version": "0.1", "books": {"1": {"title": "title", "author": "auth", '
                         '"year": 1902, "status": 2}, "2": {"title": "title2", "author": "auth2", '
                         '"year": 2000, "status": 1}, "3": {"title": "title3", "author": "auth3", '
                         '"year": 2000, "status": 1}}}')
    return reader


@pytest.fixture()
def library(json_file_wrapper):
    new_library = Library()
    new_library.load_from_json(json_file_wrapper)
    return new_library


def test_add_book_to_library_empty():
    with pytest.raises(TypeError):
        add_book_to_library(None)


def test_add_book_to_library_incomplete1(library):
    with patch("builtins.input", return_value=""):
        add_book_to_library(library)
        assert list(library.books.keys()) == [1, 2, 3]


def test_add_book_to_library_incomplete2(library):
    with patch("builtins.input", side_effect=["title", ""]):
        add_book_to_library(library)
        assert list(library.books.keys()) == [1, 2, 3]


def test_add_book_to_library_incomplete3(library):
    with patch("builtins.input", side_effect=["title", "auth", ""]):
        add_book_to_library(library)
        assert list(library.books.keys()) == [1, 2, 3]


def test_add_book_to_library_incomplete4(library):
    with patch("builtins.input", side_effect=["title", "auth", "1000", ""]):
        add_book_to_library(library)
        assert list(library.books.keys()) == [1, 2, 3]


def test_add_book_to_library_complete_with_error(library):
    with patch("builtins.input", side_effect=["title", "auth", "1000", "2000"]):
        add_book_to_library(library)
        assert list(library.books.keys()) == [1, 2, 3, 4]


def test_remove_book_from_library_empty(library):
    with pytest.raises(TypeError):
        remove_book_from_library(None)


def test_remove_book_from_library_incomplete(library):
    with patch("builtins.input", return_value=""):
        remove_book_from_library(library)
        assert list(library.books.keys()) == [1, 2, 3]


def test_remove_book_from_library_complete(library):
    with patch("builtins.input", return_value="1"):
        remove_book_from_library(library)
        assert list(library.books.keys()) == [2, 3]


def test_remove_book_from_library_error(library):
    with patch("builtins.input", return_value="1000"):
        remove_book_from_library(library)
        assert list(library.books.keys()) == [1, 2, 3]


def test_find_books_by_title_empty(library):
    with pytest.raises(TypeError):
        find_books_by_title(None)


def test_find_books_by_title_incomplete(library):
    with patch("builtins.input", return_value=""), patch("builtins.print") as mocked_print:
        find_books_by_title(library)
        assert mocked_print.call_args_list[-1].args == ("Поиск отменен",)


def test_find_books_by_title_complete1(library):
    with patch("builtins.input", return_value="title"), patch("builtins.print") as mocked_print:
        find_books_by_title(library)
        assert mocked_print.call_args_list[0].args == ('\n', 'Найдено 3 книг')


def test_find_books_by_title_complete2(library):
    with patch("builtins.input", return_value="title2"), patch("builtins.print") as mocked_print:
        find_books_by_title(library)
        assert mocked_print.call_args_list[0].args == ('\n', 'Найдено 1 книг')


def test_find_books_by_title_complete3(library):
    with patch("builtins.input", return_value="nope"), patch("builtins.print") as mocked_print:
        find_books_by_title(library)
        assert mocked_print.call_args_list[-1].args == ('Книг c подходящим названием не найдено',)


def test_find_books_by_author_empty():
    with pytest.raises(TypeError):
        find_books_by_author(None)


def test_find_books_by_author_incomplete(library):
    with patch("builtins.input", return_value=""), patch("builtins.print") as mocked_print:
        find_books_by_author(library)
        assert mocked_print.call_args_list[-1].args == ("Поиск отменен",)


def test_find_books_by_author_complete(library):
    with patch("builtins.input", return_value="auth"), patch("builtins.print") as mocked_print:
        find_books_by_author(library)
        assert mocked_print.call_args_list[0].args == ('\n', 'Найдено 3 книг')


def test_find_books_by_author_complete2(library):
    with patch("builtins.input", return_value="auth2"), patch("builtins.print") as mocked_print:
        find_books_by_author(library)
        assert mocked_print.call_args_list[0].args == ('\n', 'Найдено 1 книг')


def test_find_books_by_author_complete3(library):
    with patch("builtins.input", return_value="nope"), patch("builtins.print") as mocked_print:
        find_books_by_author(library)
        assert mocked_print.call_args_list[-1].args == ('Книг c подходящим автором не найдено',)


def test_find_books_by_year_empty():
    with pytest.raises(TypeError):
        find_books_by_year(None)


def test_find_books_by_year_incomplete(library):
    with patch("builtins.input", return_value=""), patch("builtins.print") as mocked_print:
        find_books_by_year(library)
        assert mocked_print.call_args_list[-1].args == ("Поиск отменен",)


def test_find_books_by_year_complete(library):
    with patch("builtins.input", return_value="1902"), patch("builtins.print") as mocked_print:
        find_books_by_year(library)
        assert mocked_print.call_args_list[0].args == ('\n', 'Найдено 1 книг')


def test_find_books_by_year_complete2(library):
    with patch("builtins.input", return_value="2000"), patch("builtins.print") as mocked_print:
        find_books_by_year(library)
        assert mocked_print.call_args_list[0].args == ('\n', "Найдено 2 книг")


def test_find_books_by_year_complete3(library):
    with patch("builtins.input", return_value="9999"), patch("builtins.print") as mocked_print:
        find_books_by_year(library)
        assert mocked_print.call_args_list[-1].args == ('Книг c указанным годом издания не найдено',)


def test_find_books_by_status_empty():
    with pytest.raises(TypeError):
        find_books_by_status(None)


def test_find_books_by_status_incomplete(library):
    with patch("builtins.input", return_value=""), patch("builtins.print") as mocked_print:
        find_books_by_status(library)
        assert mocked_print.call_args_list[-1].args == ("Поиск отменен",)


def test_find_books_by_status_complete(library):
    with patch("builtins.input", return_value="1"), patch("builtins.print") as mocked_print:
        find_books_by_status(library)
        assert mocked_print.call_args_list[3].args == ('\n', 'Найдено 2 книг')


def test_find_books_by_status_complete2(library):
    with patch("builtins.input", return_value="2"), patch("builtins.print") as mocked_print:
        find_books_by_status(library)
        assert mocked_print.call_args_list[3].args == ('\n', 'Найдено 1 книг')


def test_find_books_by_status_complete3(library):
    library.remove_book(1)
    with patch("builtins.input", return_value="2"), patch("builtins.print") as mocked_print:
        find_books_by_status(library)
        assert mocked_print.call_args_list[-1].args == ('Книг c указанным статусом не найдено',)


def test_show_books_empty():
    with patch("builtins.input", return_value=""), patch("builtins.print") as mocked_print:
        show_books("", {})
        assert mocked_print.call_args_list[1].args == ('Книг не найдено',)
