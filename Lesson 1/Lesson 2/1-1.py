from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import re

search = input("Введите название профессии для поиска: ")
main_link = 'https://omsk.hh.ru'
params = {'L_is_autosearch': 'false',
          'clusters': 'true',
          'enable_snippets': 'true',
          'text': f'{search}'}

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:84.0) Gecko/20100101 Firefox/84.0'}
link = 'https://omsk.hh.ru/search/vacancy?page='
page = 0
# i = 0
vacancies = []
while True:
    response = requests.get(link + str(page), params=params, headers=headers)
    soup = bs(response.text, 'html.parser')
    if response.ok:
        vacancy_list = soup.findAll('div', {'class': 'vacancy-serp-item'})
        for vacancy in vacancy_list:
            vacancy_data = {}
            vacancy_name = (vacancy.find('a'))
            vacancy_data['vacancy'] = vacancy_name.text  # Название вакансии
            vacancy_data['link'] = vacancy.find('a')['href']  # Ссылка на вакансию
            # i += 1
            salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})  # Данные о зарплате
            if salary is None:
                vacancy_data['sal_min'] = None
                vacancy_data['sal_max'] = None
                vacancy_data['currency'] = None
                # print(f'{i}){vacancy_data}')
                vacancies.append(vacancy_data)
                continue
            vacancy_data['currency'] = salary.text.split(' ')[-1]
            salary_text = ''.join(salary.text.split()[:-1])  # добавил salary_text, чтобы собрать строку без валюты
            if salary.text.find('от') > -1:
                vacancy_data['sal_min'] = re.sub('\D', '', salary_text)
                vacancy_data['sal_max'] = None
            elif salary.text.find('до') > -1:
                vacancy_data['sal_max'] = None
                vacancy_data['sal_max'] = re.sub('\D', '', salary_text)
            elif salary.text.find('-') > -1:
                vacancy_data['sal_min'] = re.sub('\D', '', salary_text.split('-')[0])
                vacancy_data['sal_max'] = re.sub('\D', '', salary_text.split('-')[-1])
            # print(f'{i}){vacancy_data}')
            vacancies.append(vacancy_data)

        page += 1
        next_button = soup.findAll('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})

        if next_button == []:
            break
print(f'{len(vacancies)} вакансий найдено')
df = pd.DataFrame(vacancies)
df.to_excel("output.xlsx")
