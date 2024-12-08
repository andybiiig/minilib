import pytest
from mock import patch
from src.utils.interface import *


def test_prompt_changer():
    assert prompt_changer(False) == ": "
    assert prompt_changer(True) == " (пустая строка для отмены): "


def test_show_menu_empty():
    assert show_menu("", {}) is None


def test_show_menu_valid():
    with patch("builtins.input", return_value="1"):
        assert show_menu("Menu", {1: "1", 2: "2"}) == 1


def test_show_menu_invalid():
    with patch("builtins.input", side_effect=["test", "8", "2"]):
        assert show_menu("Menu", {1: "1", 2: "2"}) == 2


def test_show_menu_empty_input():
    with patch("builtins.input", return_value=""):
        assert show_menu("Menu", {1: "1", 2: "2"},empty_allowed=True) is None


def test_show_table_empty():
    assert show_table("Header", []) is None


def test_show_table_no_column_headers():
    with patch('builtins.print') as mocked_print:
        show_table("Header", [["1", "2", "3"],
                              ["4", "5", "6"]])
        assert mocked_print.call_args_list[0].args == ("\n", "Header")
        assert mocked_print.call_args_list[1].args == ("+-+-+-+",)
        assert mocked_print.call_args_list[2].args == ("|1|2|3|",)
        assert mocked_print.call_args_list[3].args == ("|4|5|6|",)
        assert mocked_print.call_args_list[4].args == ("+-+-+-+",)


def test_show_table_with_column_headers():
    with patch('builtins.print') as mocked_print:
        show_table("Header", [["1", "2", "3"],
                              ["4", "5", "6"]], ["a", "b", "c"])
        assert mocked_print.call_args_list[0].args == ("\n", "Header")
        assert mocked_print.call_args_list[1].args == ("+-+-+-+",)
        assert mocked_print.call_args_list[2].args == ("|a|b|c|",)
        assert mocked_print.call_args_list[3].args == ("+-+-+-+",)
        assert mocked_print.call_args_list[4].args == ("|1|2|3|",)
        assert mocked_print.call_args_list[5].args == ("|4|5|6|",)
        assert mocked_print.call_args_list[6].args == ("+-+-+-+",)


def test_input_string_empty():
    with patch('builtins.input', return_value=""):
        assert input_string("", True) is None


def test_input_string_valid():
    with patch('builtins.input', return_value="test"):
        assert input_string("") == "test"


def test_input_string_invalid():
    with patch('builtins.input', side_effect=["", "test"]):
        assert input_string("") == "test"


def test_input_int_empty():
    with patch('builtins.input', return_value=""):
        assert input_int("", empty_allowed=True) is None


def test_input_int_valid():
    with patch('builtins.input', return_value="10"):
        assert input_int("") == 10


def test_input_int_invalid():
    # Сначала неверный ввод, потом верный - ради покрытия
    with patch('builtins.input', side_effect=["test", "5"]):
        assert input_int("") == 5


def test_input_int_invalid2():
    # Сначала неверный ввод, потом верный - ради покрытия
    with patch('builtins.input', side_effect=["10", "5"]):
        assert input_int("", max_value=8) == 5


def test_input_int_invalid3():
    # Сначала неверный ввод, потом верный - ради покрытия
    with patch('builtins.input', side_effect=["1", "10"]):
        assert input_int("", min_value=8) == 10


def test_input_int_invalid_parameters():
    with pytest.raises(ValueError) as excinfo:
        input_int("", 10, 0)
        assert str(excinfo.value) == "min_value больше max_value"


def test_print_info_unpaused_none():
    with patch('builtins.print') as mocked_print:
        print_info(None, None)
        assert mocked_print.call_args is None


def test_print_info_unpaused_message():
    with patch('builtins.print') as mocked_print:
        print_info(None, "Testing")
        assert mocked_print.call_args_list[0].args[0] == 'Testing'


def test_print_info_unpaused_info_type_message():
    with patch('builtins.print') as mocked_print:
        print_info("Error", "Testing")
        assert mocked_print.call_args_list[0].args[0] == '[Error]'
        assert mocked_print.call_args_list[1].args[0] == 'Testing'


def test_print_info_unpaused_info_type_only():
    with patch('builtins.print') as mocked_print:
        print_info("Error", None)
        assert mocked_print.call_args is None


def test_print_info_paused_none():
    with patch('builtins.input', lambda _: ''), patch('builtins.print') as mocked_print:
        print_info(None, None, True)
        assert mocked_print.call_args is None


def test_print_info_paused_message():
    with patch('builtins.input', lambda _: ''), patch('builtins.print') as mocked_print:
        print_info(None, "Testing", True)
        assert mocked_print.call_args_list[0].args[0] == 'Testing'


def test_print_info_paused_info_type_message():
    with patch('builtins.input', lambda _: ''), patch('builtins.print') as mocked_print:
        print_info("Error", "Testing", True)
        assert mocked_print.call_args_list[0].args[0] == '[Error]'
        assert mocked_print.call_args_list[1].args[0] == 'Testing'


def test_print_info_paused_info_type_only():
    with patch('builtins.input', lambda _: ''), patch('builtins.print') as mocked_print:
        print_info("Error", None, True)
        assert mocked_print.call_args is None
