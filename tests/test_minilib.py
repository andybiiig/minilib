import io

import pytest
from mock import patch, mock_open
from src.minilib import *


jsoned_lib = '{"lib_version": "0.1", "books": {"1": {"title": "title", "author": "auth", ' \
    '"year": 1902, "status": 2}, "2": {"title": "title2", "author": "auth2", ' \
    '"year": 2000, "status": 1}, "3": {"title": "title3", "author": "auth3", ' \
    '"year": 2000, "status": 1}}}'

@pytest.fixture()
def json_file_wrapper():
    reader = io.StringIO(jsoned_lib)
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


def test_load_library_correct():
    new_library = Library()
    with patch("builtins.open", mock_open(read_data=jsoned_lib)):
        load_library(new_library)
        assert new_library.get_all_ids() == [1, 2, 3]

def test_load_library_incorrect_type():
    with pytest.raises(TypeError):
        load_library(None)


def test_load_library_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError), patch("src.minilib.print_info") as mocked_print:
        load_library(Library())
        assert mocked_print.call_args_list[0].args == ('ИНФОРМАЦИЯ', 'Файл ../library.json не найден, запуск считается первичным')

def test_load_library_incorrect_file():
    with patch("builtins.open", mock_open(read_data="incorrect data")), patch("src.minilib.print_info"):
        with pytest.raises(SystemExit):
            load_library(Library())

def test_load_library_incorrect_data():
    with patch("builtins.open", mock_open(read_data=jsoned_lib.replace("0.1", "0.2"))), patch("src.minilib.print_info"):
        with pytest.raises(SystemExit):
            load_library(Library())

def test_save_library_correct(library):
    with patch("builtins.open", mock_open()) as mocked_file:
        library.changed = True
        save_library(library)
        mocked_file.assert_called_with("../library.json", "w", encoding="utf-8")

def test_save_library_incorrect():
    with pytest.raises(TypeError):
        save_library(None)

def test_save_library_unchanged(library):
    with patch("builtins.open", mock_open()) as mocked_file:
        save_library(library)
        assert not mocked_file.called

def test_save_library_file_error(library):
    with patch("builtins.open", side_effect=PermissionError), patch("src.minilib.print_info"):
        with pytest.raises(SystemExit):
            library.changed = True
            save_library(library)

def test_do_main_cycle_incorrect():
    with pytest.raises(TypeError):
        do_main_cycle(None)

def test_do_main_cycle_correct0(library):
    with patch("src.minilib.show_menu", return_value=0):
        do_main_cycle(library)
        assert library.get_all_ids() == [1, 2, 3]

def test_do_main_cycle_correct1(library):
    with patch("src.minilib.show_menu", side_effect=[1, 0]), patch("src.minilib.add_book_to_library") as mocked_func:
        do_main_cycle(library)
        assert mocked_func.call_count == 1

def test_do_main_cycle_correct2(library):
    with patch("src.minilib.show_menu", side_effect=[2, 0]), patch("src.minilib.remove_book_from_library") as mocked_func:
        do_main_cycle(library)
        assert mocked_func.call_count == 1

def test_do_main_cycle_correct3(library):
    with patch("src.minilib.show_menu", side_effect=[3, 0]), patch("src.minilib.find_books") as mocked_func:
        do_main_cycle(library)
        assert mocked_func.call_count == 1

def test_do_main_cycle_correct4(library):
    with patch("src.minilib.show_menu", side_effect=[4, 0]), patch("src.minilib.show_books") as mocked_func:
        do_main_cycle(library)
        assert mocked_func.call_count == 1

def test_do_main_cycle_correct5(library):
    with patch("src.minilib.show_menu", side_effect=[5, 0]), patch("src.minilib.change_book_status") as mocked_func:
        do_main_cycle(library)
        assert mocked_func.call_count == 1

def test_find_books_incorrect():
    with pytest.raises(TypeError):
        find_books(None)

def test_find_books_correct0(library):
    with patch("src.minilib.show_menu", return_value=None):
        find_books(library)
        assert library.get_all_ids() == [1, 2, 3]

def test_find_books_correct1(library):
    with patch("src.minilib.show_menu", side_effect=[1, None]), patch("src.minilib.find_books_by_title") as mocked_func:
        find_books(library)
        assert mocked_func.call_count == 1

def test_find_books_correct2(library):
    with patch("src.minilib.show_menu", side_effect=[2, None]), patch("src.minilib.find_books_by_author") as mocked_func:
        find_books(library)
        assert mocked_func.call_count == 1

def test_find_books_correct3(library):
    with patch("src.minilib.show_menu", side_effect=[3, None]), patch("src.minilib.find_books_by_year") as mocked_func:
        find_books(library)
        assert mocked_func.call_count == 1

def test_find_books_correct4(library):
    with patch("src.minilib.show_menu", side_effect=[4, None]), patch("src.minilib.find_books_by_status") as mocked_func:
        find_books(library)
        assert mocked_func.call_count == 1

def test_change_book_status_incorrect():
    with pytest.raises(TypeError):
        change_book_status(None)

def test_change_book_status_unchanged(library):
    with patch("src.minilib.input_int", return_value=None), patch("src.minilib.print_info") as mocked_print:
        change_book_status(library)
        assert mocked_print.call_args_list[0].args == ('ИНФОРМАЦИЯ', 'Изменение статуса книги отменено')

def test_change_book_status_incorrect_id(library):
    with patch("src.minilib.input_int", return_value=4), patch("src.minilib.print_info") as mocked_print:
        change_book_status(library)
        assert mocked_print.call_args_list[0].args == ('ОШИБКА', 'Книг с таким id не найдено', True)

def test_change_book_status_correct_id_no_status(library):
    with (patch("src.minilib.input_int", return_value=1),
          patch("src.minilib.show_menu", return_value=None),
          patch("src.minilib.print_info") as mocked_print):
        change_book_status(library)
        assert mocked_print.call_args_list[0].args == ('ИНФОРМАЦИЯ', 'Изменение статуса книги отменено')

def test_change_book_status_correct_id_incorrect_status(library):
    with (patch("src.minilib.input_int", return_value=1),
          patch("src.minilib.show_menu", return_value=5),
          patch("src.minilib.print_info") as mocked_print):
        with pytest.raises(ValueError):
            change_book_status(library)

def test_change_book_status_correct_id_correct_status(library):
    with (patch("src.minilib.input_int", return_value=1),
          patch("src.minilib.show_menu", return_value=1),
          patch("src.minilib.print_info") as mocked_print):

         change_book_status(library)
         assert mocked_print.call_args_list[0].args == ('ИНФОРМАЦИЯ', 'Статус книги изменен')

