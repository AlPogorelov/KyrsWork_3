from abc import ABC, abstractmethod

import requests


class AbstractHeadHunter(ABC):

    def connect_API(self):
        pass

    def get_employer_id(self, *args):
        pass


class HeadHunterAPIEmployers(AbstractHeadHunter):

    def __init__(self):
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "employer_id": "", "page": 0, "per_page": 100}
        self.vacancies = []

    def __connect_API(self):
        '''Модель подключения к API и обработка ошибок запроса'''
        try:
            response = requests.get(
                self.__url, headers=self.__headers, params=self.__params
            )
            if response.status_code != 200:

                print(f"Ошибка запроса API: {response.status_code}")

            return response

        except requests.exceptions.RequestException as e:
            # Обработка ошибок запроса
            print(f"Ошибка при выполнении запроса: {e}")
            return None

    def get_employer_id(self, employers):
        '''Получает список ключевых слов по компании и находит employer_id этой компании
         и выдает список ID по списку компаний'''

        self.__url = "https://api.hh.ru/employers/"

        employers_id = []
        for employer in employers:
            self.__params["text"] = employer
            response = self.__connect_API()
            employer_id = response.json()["items"][0]
            employer_dict = {'employer_id': employer_id['id'],
                             'employer_name': employer_id['name'],
                             'vacancies_url': employer_id['vacancies_url']}
            employers_id.append(employer_dict)
        return employers_id

    def get_vac_by_employer(self, employers_id):
        '''Получая на вход спискок компаний с ID, плучаем список вакансий этих компаний'''
        vac_list_all_empl = []

        for employer in employers_id:
            self.__url = employer['vacancies_url']
            self.__params = {"page": 0, "per_page": 100, 'only_with_salary': 'true'}
            response = self.__connect_API()
            vac_employer = response.json()['items']
            for vac in vac_employer:
                vac_dict = {'vacancies_name': vac['name'],
                            'city': vac['area']['name'],
                            'salary': vac.get('salary', '').get('from', 0),
                            'requirement': vac['snippet']['requirement'],
                            'responsibility': vac['snippet']['responsibility'],
                            'url': vac['alternate_url'],
                            'employer_id': vac['employer']['id']}
                vac_list_all_empl.append(vac_dict)

        return vac_list_all_empl


