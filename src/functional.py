import json
import os
import requests
from bs4 import BeautifulSoup
import time
from requests.exceptions import RequestException


class Vacancy:
    """Класс для представления вакансии"""
    __slots__ = ['title', 'url', 'salary', 'description', 'address']

    def __init__(self, title, url, salary, description, address):
        """ Инициализация объекта Vacancy"""
        self.title = title
        self.url = url
        self.salary = self._validate_salary(salary)
        self.description = description
        self.address = self._validate_address(address)

    def _validate_salary(self, salary):
        """ Валидация зарплаты"""
        if not salary:
            return "Зарплата не указана"
        return salary

    def _validate_address(self, address):
        """Валидация адреса"""
        if not address:
            return "Адрес не указан"
        return address

    def __lt__(self, other):
        """Метод для сравнения вакансий по зарплате"""
        if isinstance(other, Vacancy):
            return self.salary < other.salary
        return NotImplemented

    def __str__(self):
        """Строковое представление вакансии"""
        return (f"Профессия-З/П: {self.title} - {self.salary}\n"
                f"Ссылка: {self.url}\n"
                f"Адрес: {self.address}\n"
                f"Описание: {self.description[:200]}...\n")

    def to_dict(self):
        """Преобразование вакансии в словарь"""
        return {
            "title": self.title,
            "url": self.url,
            "salary": self.salary,
            "description": self.description,
            "address": self.address
        }


def get_vacancy_description(url):
    """Получение описания вакансии по URL"""
    max_retries = 3
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            description = soup.find('div', {'data-qa': 'vacancy-description'})
            if not description:
                description = soup.find('div', {'class': 'vacancy-description'})
            if not description:
                description = soup.find('div', {'class': 'g-user-content'})

            if description:
                return description.text.strip()
            else:
                return "Описание не найдено"
        except RequestException as e:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                return "Описание недоступно"


class JSONSaver:
    """Класс для сохранения вакансий в JSON файл"""
    @staticmethod
    def save_vacancies(vacancies, filename):
        """Сохранение списка вакансий в JSON файл"""
        if not os.path.exists("C:/Users/Александр Побережный/Desktop/питон/OOP/Course_work_OOP/data"):
            os.makedirs("C:/Users/Александр Побережный/Desktop/питон/OOP/Course_work_OOP/data")

        file_path = os.path.join("C:/Users/Александр Побережный/Desktop/питон/OOP/Course_work_OOP/data", filename)

        vacancies_data = [vacancy.to_dict() for vacancy in vacancies]

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(vacancies_data, file, ensure_ascii=False, indent=4)

        print(f"Вакансии сохранены в файл: {file_path}")
