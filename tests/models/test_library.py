import io
from json import JSONDecodeError

import pytest
from src.models.library import Library, CompatibilityError
from src.models.book import Book


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


@pytest.fixture()
def book():
    return Book(title="Test Title", author="Test Author", year=2020)


def test_get_changed_false(library):
    # Библиотека только что загружена
    assert library.get_changed() is False


def test_get_changed_false2(library, book):
    # Меняем статус на тот же самый
    library.change_book_status(1, 2)
    assert library.get_changed() is False


def test_get_changed_true1(library,book):
    library.add_book(book)
    assert library.get_changed() is True


def test_get_changed_true2(library, book):
    library.remove_book(1)
    assert library.get_changed() is True


def test_get_changed_true3(library, book):
    library.change_book_status(1, 1)
    assert library.get_changed() is True


def test_get_book_valid(library):
    assert library.get_book(1).to_dict() == {'title': 'title', 'author': 'auth',  'year': 1902, 'status': 2}


def test_get_book_invalid(library):
    with pytest.raises(KeyError):
        library.get_book(4)


def test_add_book_valid(library, book):
    new_id = library.next_id
    library.add_book(book)
    assert library.get_book(new_id) == book


def test_add_book_invalid(library):
    with pytest.raises(TypeError):
        library.add_book(None)


def test_get_all_ids(library):
    assert library.get_all_ids() == [1, 2, 3]


def test_get_all_books(library):
    assert list(library.get_all_books().keys()) == [1, 2, 3]


def test_find_books_by_author1(library):
    assert list(library.find_books_by_author('auth').keys()) == [1, 2, 3]


def test_find_books_by_author2(library):
    assert list(library.find_books_by_author('auth2').keys()) == [2]


def test_find_books_by_author3(library):
    assert list(library.find_books_by_author('auth4').keys()) == []


def test_find_books_by_title1(library):
    assert list(library.find_books_by_title('title').keys()) == [1, 2, 3]


def test_find_books_by_title2(library):
    assert list(library.find_books_by_title('title2').keys()) == [2]


def test_find_books_by_title3(library):
    assert list(library.find_books_by_title('title4').keys()) == []


def test_find_books_by_year1(library):
    assert list(library.find_books_by_year(2000).keys()) == [2, 3]


def test_find_books_by_year2(library):
    assert list(library.find_books_by_year(2001).keys()) == []


def test_find_books_by_status1(library):
    assert list(library.find_books_by_status(1).keys()) == [2, 3]


def test_find_books_by_status2(library):
    assert list(library.find_books_by_status(2).keys()) == [1]


def test_find_books_by_status3(library):
    assert list(library.find_books_by_status(3).keys()) == []


def test_change_book_status_valid(library):
    library.change_book_status(1, 1)
    assert library.get_book(1).status == 1


def test_change_book_status_invalid(library):
    with pytest.raises(KeyError):
        library.change_book_status(4, 1)


def test_remove_book_valid(library):
    library.remove_book(1)
    assert library.get_all_ids() == [2, 3]


def test_remove_book_invalid(library):
    with pytest.raises(KeyError):
        library.remove_book(4)


def test_load_from_json_invalid1(library):
    reader = io.StringIO()
    with pytest.raises(JSONDecodeError):
        library.load_from_json(reader)


def test_load_from_json_invalid2(library):
    reader = io.StringIO('{"books": {"1": {"title": "title", "author": "auth", '
                         '"year": 1902, "status": 2}, "2": {"title": "title2", "author": "auth2", '
                         '"year": 2000, "status": 1}, "3": {"title": "title3", "author": "auth3", '
                         '"year": 2000, "status": 1}}}')
    with pytest.raises(TypeError):
        library.load_from_json(reader)


def test_load_from_json_invalid3(library):
    reader = io.StringIO('{"lib_version": "0.2", "books": {"1": {"title": "title", "author": "auth", '
                         '"year": 1902, "status": 2}, "2": {"title": "title2", "author": "auth2", '
                         '"year": 2000, "status": 1}, "3": {"title": "title3", "author": "auth3", '
                         '"year": 2000, "status": 1}}}')
    with pytest.raises(CompatibilityError):
        library.load_from_json(reader)


def test_load_from_json_invalid4(library):
    reader = io.StringIO('{"lib_version": "0.1"}')
    with pytest.raises(TypeError):
        library.load_from_json(reader)


def test_save_to_json(library, json_file_wrapper):
    writer = io.StringIO()
    library.save_to_json(writer)
    assert writer.getvalue() == json_file_wrapper.getvalue()

