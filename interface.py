from main import *


def interface():
    """Функция создания интерфейса для пользователя"""
    print('Приветствую')
    user_input = input('С какой платформы будем смотреть вакансии?(hh или sj): ')
    while user_input != 'hh' and user_input != 'sj':
        user_input = input('Введите hh или sj: ')
    if user_input.lower() == 'hh':
        jobs = HH()
    elif user_input.lower() == 'sj':
        jobs = Superjobs()


    a = input('Введите название искомой работы: ')
    b = input('Введите номер страницы: ')
    jobs.get_vacancies(a, int(b))
    page_history = []
    page_history.append(b)
    while True:
        c = input('\nМожем: \n1 - просмотреть требования к вакансиям\n2 - открыть другую страницу\nили\n3- записать список данных вакансий в файл\n'
                  'Для выхода введите exit\nВвод: ')
        if c == 'exit':
            break
        try:
            if int(c) == 1:
                d = input('Введите номер вакансии: ')
                jobs.requirements(int(d))
            elif int(c) == 2:
                d = input('Введите номер страницы: ')
                if d in page_history:
                    print('\nЭта страница уже выведена')
                else:
                    page_history.append(d)
                    jobs.get_vacancies(a, int(d))
            elif int(c) == 3:
                d = input('Введите название файла: ')
                jobs.to_file(str(d))
                print('\nФайл записан')
            else:
                print('\nВыберите вариант из списка или введите exit')
        except ValueError:
            print('\nВыберите вариант из списка или введите exit')



interface()


