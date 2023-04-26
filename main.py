import os

import requests
import json
from abc import ABC, abstractmethod


class AbReq(ABC):
    """Абстрактный класс для классов по работе с API платформ"""
    @abstractmethod
    def get_vacancies(self):
        """Абстрактный метод для работы с API платформ для поиска вакансий"""
        pass

    @abstractmethod
    def to_file(self):
        """Абстрактный метод для записи в файл"""
        pass



class HH(AbReq):
    """Класс для работы с API HH"""

    def __init__(self):
        self.response_json = None
        self.counter = 0
        self.reqs = []
        self.results = {}

    def get_vacancies(self, user_input, page_number=0):
        """Метод для работы с API платформ для поиска вакансий"""
        if page_number == 0:
            print(f'Страница: {page_number + 1}')
            page_number = 1
        else:
            print(f'Страница: {page_number}')
        response = requests.get('https://api.hh.ru/vacancies', params={'text': user_input, 'page': page_number - 1,
                                                                     'per_page': 100})
        self.response_json = response.json()
        try:
            for i in self.response_json['items']:
                self.counter += 1

                self.reqs.append({self.counter: i['snippet']['requirement']})
                self.reqs.append({self.counter: i['snippet']['responsibility']})
                if i['salary'] is None:
                    try:
                        if i['address']['city'] is None:
                            answer = f"{self.counter}.{i['name']}, оплата не указана, город не указан, ссылка на вакансию: {i['alternate_url']}"
                            print(answer)
                            self.results[self.counter] = answer
                        else:
                            answer = f"{self.counter}.{i['name']}, оплата не указана, город:{i['address']['city']}, ссылка на вакансию: {i['alternate_url']}"
                            print(answer)
                            self.results[self.counter] = answer
                    except TypeError:
                        answer = f"{self.counter}.{i['name']}, оплата не указана, город не указан, ссылка на вакансию: {i['alternate_url']}"
                        print(answer)
                        self.results[self.counter] = answer
                elif i['salary']['from'] is None:
                    try:
                        if i['address']['city'] is None:
                            answer = f"{self.counter}.{i['name']}, оплата: {i['salary']['to']}, город не указан, ссылка на вакансию: {i['alternate_url']}"
                            print(answer)
                            self.results[self.counter] = answer
                        else:
                            answer = f"{self.counter}.{i['name']}, оплата: {i['salary']['to']}, город:{i['address']['city']}, ссылка на вакансию: {i['alternate_url']}"
                            print(answer)
                            self.results[self.counter] = answer
                    except TypeError:
                        answer = f"{self.counter}.{i['name']}, оплата: {i['salary']['to']}, город не указан, ссылка на вакансию: {i['alternate_url']}"
                        print(answer)
                        self.results[self.counter] = answer
                elif i['salary']['to'] is None:
                    try:
                        if i['address']['city'] is None:
                            answer = f"{self.counter}.{i['name']}, оплата: {i['salary']['from']}, город не указан, ссылка на вакансию: {i['alternate_url']}"
                            print(answer)
                            self.results[self.counter] = answer
                        else:
                            answer = f"{self.counter}.{i['name']}, оплата: {i['salary']['from']}, город:{i['address']['city']}, ссылка на вакансию: {i['alternate_url']}"
                            print(answer)
                            self.results[self.counter] = answer
                    except TypeError:
                        answer = f"{self.counter}.{i['name']}, оплата: {i['salary']['from']}, город не указан, ссылка на вакансию: {i['alternate_url']}"
                        print(answer)
                        self.results[self.counter] = answer
                else:
                    try:
                        if i['address']['city'] is None:
                            answer = f"{self.counter}.{i['name']}, оплата: {i['salary']['from']} - {i['salary']['to']}, город не указан, ссылка на вакансию: {i['alternate_url']}"
                            print(answer)
                            self.results[self.counter] = answer
                        else:
                            answer = f"{self.counter}.{i['name']}, оплата: {i['salary']['from']} - {i['salary']['to']}, город: {i['address']['city']}, ссылка на вакансию: {i['alternate_url']}"
                            print(answer)
                            self.results[self.counter] = answer
                    except TypeError:
                        answer = f"{self.counter}.{i['name']}, оплата: {i['salary']['from']} - {i['salary']['to']}, город не указан, ссылка на вакансию: {i['alternate_url']}"
                        print(answer)
                        self.results[self.counter] = answer
        except KeyError:
            print('Превышено количство страниц')

    def requirements(self, vac_num=1):
        """Метод для прсомотра требований к вакансиям"""
        for i in self.reqs:
            if vac_num in i.keys():
                print(i[vac_num])

    #def sort_by_salary(self):
    #    sal = [i['salary']['from'] for i in self.response_json['items']]
    #    print(sal)


    def to_file(self, file_name = 'vacancies'):
        """Метод для записи в файл"""
        with open(file_name + '.json', 'w', encoding='UTF-8') as file:
            json.dump(self.results, file, indent=2, ensure_ascii=False)

class Superjobs(AbReq):
    """Класс для работы с API Superjobs"""

    def __init__(self ):
        self.response_json = None
        self.counter = 0
        self.reqs = []
        self.results = {}

    def get_vacancies(self, user_input, page_number=1):
        """Метод для работы с API платформ для поиска вакансий"""
        if page_number == 0:
            print(f'Страница: {page_number + 1}')
            page_number = 1
        else:
            print(f'Страница: {page_number}')
        headers = {"X-Api-App-Id": os.getenv('SJ_API')}
        response = requests.get('https://api.superjob.ru/2.0/vacancies/', headers=headers,
                                params={'keyword': user_input, 'page': page_number, 'count': 100})
        self.response_json = response.json()
        if len(self.response_json['objects']) > 0:
            for i in self.response_json['objects']:
                self.counter += 1

                try:
                    self.reqs.append({self.counter: i['candidat'] + i['type_of_work']['title'] + i['place_of_work']['title']})
                except TypeError:
                    self.reqs.append({self.counter: i['candidat']})
                if i['payment_from'] == 0 and i['payment_to'] == 0:
                    answer = f"{self.counter}.{i['profession']}, оплата не указана, город: {i['town']['title']}, ссылка на вакансию: {i['link']}"
                    print(answer)
                    self.results[self.counter] = answer
                elif i['payment_from'] == 0:
                    answer = f"{self.counter}.{i['profession']}, оплата: до {i['payment_to']}, город: {i['town']['title']}, ссылка на вакансию: {i['link']}"
                    print(answer)
                    self.results[self.counter] = answer
                elif i['payment_to'] == 0:
                    answer = f"{self.counter}.{i['profession']}, оплата: от {i['payment_from']}, город: {i['town']['title']}, ссылка на вакансию: {i['link']}"
                    print(answer)
                    self.results[self.counter] = answer
                else:
                    answer = f"{self.counter}.{i['profession']}, оплата: от {i['payment_from']} до {i['payment_to']}, город: {i['town']['title']}, ссылка на вакансию: {i['link']}"
                    print(answer)
                    self.results[self.counter] = answer
        else:
            print('Превышено количство страниц')


    def requirements(self, vac_num=1):
        """Метод для прсомотра требований к вакансиям"""
        for i in self.reqs:
            if vac_num in i.keys():
                print(i[vac_num])

    def to_file(self, file_name= 'vacancies'):
        """Метод для записи в файл"""
        with open(file_name + '.json', 'w', encoding='UTF-8') as file:
            json.dump(self.results, file, indent=2, ensure_ascii=False)


