from src.API_client import HeadHunterAPI
from src.functional import get_vacancy_description
from src.classes import Vacancy, JSONSaver
from typing import List


def get_vacancies_from_hh(keyword: str) -> List[Vacancy]:
    """Получение вакансий с HeadHunter по ключевому слову"""
    hh_api = HeadHunterAPI()
    vacancies_data = hh_api.get_vacancies(keyword)

    vacancies = []
    for item in vacancies_data:
        title = item["name"]
        url = item["alternate_url"]
        salary = item["salary"]["from"] if item["salary"] and item["salary"]["from"] else None
        description = get_vacancy_description(url)
        address = item["address"]["raw"] if item["address"] else None

        vacancy = Vacancy(title, url, salary, description, address)
        vacancies.append(vacancy)

    return vacancies


def user_interaction() -> None:
    """Функция для взаимодействия с пользователем через консоль"""
    while True:
        print("\nМеню:")
        print("1. Поиск вакансий")
        print("2. Показать топ N вакансий по зарплате")
        print("3. Поиск вакансий по ключевому слову и сохранение в JSON")
        print("4. Выход")

        choice = input("Выберите действие (1-4): ")

        if choice == "1":
            keyword = input("Введите поисковый запрос: ")
            vacancies = get_vacancies_from_hh(keyword)
            print(f"Найдено {len(vacancies)} вакансий.")
            for vacancy in vacancies[:10]:
                print(vacancy)

        elif choice == "2":
            keyword = input("Введите поисковый запрос: ")
            vacancies = get_vacancies_from_hh(keyword)
            n = int(input("Введите количество вакансий для отображения: "))
            sorted_vacancies = sorted(vacancies, key=lambda x: x.salary if isinstance(x.salary, (int, float)) else 0,
                                      reverse=True)
            for vacancy in sorted_vacancies[:n]:
                print(vacancy)

        elif choice == "3":
            keyword = input("Введите поисковый запрос: ")
            vacancies = get_vacancies_from_hh(keyword)
            search_word = input("Введите ключевое слово для поиска в описании: ")
            filtered_vacancies = [v for v in vacancies if search_word.lower() in v.description.lower()]
            if filtered_vacancies:
                JSONSaver.save_vacancies(filtered_vacancies, f"{keyword}_{search_word}_vacancies.json")
            else:
                print("Не найдено вакансий с указанным ключевым словом в описании.")

        elif choice == "4":
            print("До свидания!")
            break

        else:
            print("Неверный выбор. Пожалуйста, выберите число от 1 до 4.")


if __name__ == "__main__":
    user_interaction()
