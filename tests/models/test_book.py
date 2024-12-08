import pytest
from src.models.book import Book

@pytest.fixture()
def book():
    return Book(title="Test Title", author="Test Author", year=2020)


def test_get_title(book):
    assert book.get_title() == "Test Title"


def test_get_author(book):
    assert book.get_author() == "Test Author"


def test_get_year(book):
    assert book.get_year() == 2020


def test_get_status(book):
    assert book.get_status() == 1


def test_set_status(book):
    book.set_status(2)
    assert book.get_status() == 2


def test_set_status_invalid(book):
    with pytest.raises(ValueError):
        book.set_status(3)


def test_set_status_invalid_type(book):
    with pytest.raises(TypeError):
        book.set_status("0")


def test_set_status_invalid_type_2(book):
    with pytest.raises(TypeError):
        book.set_status(2.0)


def test_to_dict(book):
    assert book.to_dict() == {
        "title": "Test Title",
        "author": "Test Author",
        "year": 2020,
        "status": 1
    }
