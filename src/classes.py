import json
import os
from typing import List, Dict, Optional


class Vacancy:
    """Класс для представления вакансии"""
    __slots__ = ['title', 'url', 'salary', 'description', 'address']

    def __init__(self, title: str, url: str, salary: Optional[int], description: str, address: Optional[str]):
        """ Инициализация объекта Vacancy"""
        self.title: str = title
        self.url: str = url
        self.salary: str = self._validate_salary(salary)
        self.description: str = description
        self.address: str = self._validate_address(address)

    def _validate_salary(self, salary: Optional[int]) -> str:
        """ Валидация зарплаты"""
        if not salary:
            return "Зарплата не указана"
        return str(salary)

    def _validate_address(self, address: Optional[str]) -> str:
        """Валидация адреса"""
        if not address:
            return "Адрес не указан"
        return address

    def __lt__(self, other: 'Vacancy') -> bool:
        """Метод для сравнения вакансий по зарплате"""
        if isinstance(other, Vacancy):
            return self.salary < other.salary
        return NotImplemented

    def __str__(self) -> str:
        """Строковое представление вакансии"""
        return (f"Профессия-З/П: {self.title} - {self.salary}\n"
                f"Ссылка: {self.url}\n"
                f"Адрес: {self.address}\n"
                f"Описание: {self.description[:200]}...\n")

    def to_dict(self) -> Dict[str, str]:
        """Преобразование вакансии в словарь"""
        return {
            "title": self.title,
            "url": self.url,
            "salary": self.salary,
            "description": self.description,
            "address": self.address
        }


class JSONSaver:
    """Класс для сохранения вакансий в JSON файл"""
    @staticmethod
    def save_vacancies(vacancies: List[Vacancy], filename: str) -> None:
        """Сохранение списка вакансий в JSON файл"""
        if not os.path.exists("C:/Users/Александр Побережный/Desktop/питон/OOP/Course_work_OOP/data"):
            os.makedirs("C:/Users/Александр Побережный/Desktop/питон/OOP/Course_work_OOP/data")

        file_path = os.path.join("C:/Users/Александр Побережный/Desktop/питон/OOP/Course_work_OOP/data", filename)

        vacancies_data = [vacancy.to_dict() for vacancy in vacancies]

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(vacancies_data, file, ensure_ascii=False, indent=4)

        print(f"Вакансии сохранены в файл: {file_path}")
