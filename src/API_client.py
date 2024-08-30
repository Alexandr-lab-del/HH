import requests
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class APIClient(ABC):
    """Абстрактный базовый класс для API-клиентов"""
    @abstractmethod
    def get_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        """ Абстрактный метод для получения вакансий"""
        pass


class HeadHunterAPI(APIClient):
    """ Класс для работы с API HeadHunter"""
    def __init__(self):
        """Инициализация объекта HeadHunterAPI"""
        self.base_url: str = "https://api.hh.ru/vacancies"
        self.headers: Dict[str, str] = {"User-Agent": "HH-User-Agent"}

    def get_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        """Получение вакансий с HeadHunter по ключевому слову"""
        params = {
            "text": keyword,
            "per_page": 100
        }
        response = requests.get(self.base_url, headers=self.headers, params=params)
        return response.json()["items"]
