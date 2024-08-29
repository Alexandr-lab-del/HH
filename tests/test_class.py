import pytest
from unittest.mock import patch, MagicMock
from src.API_client import HeadHunterAPI
from main import (get_vacancies_from_hh, user_interaction)
from src.functional import (Vacancy, get_vacancy_description, JSONSaver)


@pytest.fixture
def sample_vacancy():
    """Фикстура, создающая образец вакансии для тестирования"""
    return Vacancy(
        title="Python Developer",
        url="https://hh.ru/vacancy/123456",
        salary=100000,
        description="We are looking for a Python developer...",
        address="Moscow, Russia"
    )


def test_headhunter_api():
    """Тестирует метод get_vacancies класса HeadHunterAPI"""
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {"items": [{"name": "Test Vacancy"}]}
        api = HeadHunterAPI()
        vacancies = api.get_vacancies("Python")
        assert len(vacancies) == 1
        assert vacancies[0]["name"] == "Test Vacancy"


def test_vacancy_init(sample_vacancy):
    """Проверяет правильность инициализации объекта Vacancy"""
    assert sample_vacancy.title == "Python Developer"
    assert sample_vacancy.url == "https://hh.ru/vacancy/123456"
    assert sample_vacancy.salary == 100000
    assert sample_vacancy.description == "We are looking for a Python developer..."
    assert sample_vacancy.address == "Moscow, Russia"


def test_vacancy_validate_salary():
    """Проверяет валидацию зарплаты в классе Vacancy"""
    vacancy_no_salary = Vacancy("Test", "http://test.com", None, "Description",
                                "Address")
    assert vacancy_no_salary.salary == "Зарплата не указана"


def test_vacancy_validate_address():
    """ Проверяет валидацию адреса в классе Vacancy"""
    vacancy_no_address = Vacancy("Test", "http://test.com", 100000, "Description", None)
    assert vacancy_no_address.address == "Адрес не указан"


def test_vacancy_lt():
    """Тестирует метод __lt__ класса Vacancy"""
    v1 = Vacancy("Test1", "http://test1.com", 100000, "Description1", "Address1")
    v2 = Vacancy("Test2", "http://test2.com", 200000, "Description2", "Address2")
    assert v1 < v2


def test_vacancy_str(sample_vacancy):
    """Проверяет строковое представление объекта Vacancy"""
    vacancy_str = str(sample_vacancy)
    assert "Python Developer" in vacancy_str
    assert "100000" in vacancy_str
    assert "https://hh.ru/vacancy/123456" in vacancy_str


def test_vacancy_to_dict(sample_vacancy):
    """Тестирует метод to_dict класса Vacancy"""
    vacancy_dict = sample_vacancy.to_dict()
    assert vacancy_dict["title"] == "Python Developer"
    assert vacancy_dict["salary"] == 100000


@patch('requests.get')
def test_get_vacancy_description(mock_get):
    """Тестирует функцию get_vacancy_description"""
    mock_response = MagicMock()
    mock_response.content = '<div data-qa="vacancy-description">Test Description</div>'
    mock_get.return_value = mock_response

    description = get_vacancy_description("https://test.com")
    assert description == "Test Description"


@patch('main.HeadHunterAPI.get_vacancies')
@patch('main.get_vacancy_description')
def test_get_vacancies_from_hh(mock_get_description, mock_get_vacancies):
    """Тестирует функцию get_vacancies_from_hh"""
    mock_get_vacancies.return_value = [
        {
            "name": "Test Vacancy",
            "alternate_url": "https://test.com",
            "salary": {"from": 100000},
            "address": {"raw": "Test Address"}
        }
    ]
    mock_get_description.return_value = "Test Description"

    vacancies = get_vacancies_from_hh("Python")
    assert len(vacancies) == 1
    assert vacancies[0].title == "Test Vacancy"
    assert vacancies[0].salary == 100000


@patch('json.dump')
@patch('os.path.exists')
@patch('os.makedirs')
def test_json_saver(mock_makedirs, mock_exists, mock_dump, sample_vacancy):
    """Тестирует метод save_vacancies класса JSONSaver"""
    mock_exists.return_value = False

    JSONSaver.save_vacancies([sample_vacancy], "test.json")

    mock_makedirs.assert_called_once()
    mock_dump.assert_called_once()


@patch('builtins.input')
@patch('main.get_vacancies_from_hh')
@patch('main.JSONSaver.save_vacancies')
def test_user_interaction(mock_save_vacancies, mock_get_vacancies, mock_input):
    """Тестирует функцию user_interaction для сценария без сохранения в JSON файл"""
    mock_input.side_effect = ["1", "Python", "4"]
    mock_get_vacancies.return_value = [
        Vacancy("Python Dev", "http://test.com", 100000, "Description", "Address")
    ]

    user_interaction()

    mock_get_vacancies.assert_called_once_with("Python")
    mock_save_vacancies.assert_not_called()


@patch('builtins.input')
@patch('main.get_vacancies_from_hh')
@patch('main.JSONSaver.save_vacancies')
def test_user_interaction_save_json(mock_save_vacancies, mock_get_vacancies, mock_input):
    """Тестирует функцию user_interaction для сценария с сохранением в JSON файл"""
    mock_input.side_effect = ["3", "Python", "developer", "4"]
    mock_get_vacancies.return_value = [
        Vacancy("Python Dev", "http://test.com", 100000, "We need a Python developer",
                "Address")
    ]

    user_interaction()

    mock_get_vacancies.assert_called_once_with("Python")
    mock_save_vacancies.assert_called_once()


@patch('builtins.input')
@patch('main.get_vacancies_from_hh')
def test_user_interaction_invalid_choice(mock_get_vacancies, mock_input):
    """Тестирует функцию user_interaction при вводе недопустимого варианта"""
    mock_input.side_effect = ["5", "4"]

    user_interaction()

    mock_get_vacancies.assert_not_called()
