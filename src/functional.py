import requests
from bs4 import BeautifulSoup
import time
from requests.exceptions import RequestException


def get_vacancy_description(url: str) -> str:
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
