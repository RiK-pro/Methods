from pymongo import MongoClient
from pprint import pprint
import json

client = MongoClient('127.0.0.1', 27017)
db = client['headhunter']  # база данных "headhunter"

vacancies = db.vacancies  # Переменная vacancies. db.vacancies - коллекция


# Функция, записывающая собранные вакансии в созданную БД
def add_new_vac(db, read_job):
    for el in read_job:
        link = el["link"]
        if vacancies.count_documents({"link": link}) == 0:  # проверяем новые вакансии по уникальному полю link.
            vacancies.insert_one(el)  # Если в бд не повторяется, то добавляем


# Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы.
# Поиск должен происходить по 2-ум полям (минимальной и максимальной зарплате)
def max_salary(how_much):
    for job in vacancies.find({'$or': [{'sal_min': {'$gt': how_much}}, {'sal_max': {'$gt': how_much}}]}):
        pprint(job)


with open("result.json", "r") as read_job:
    read_job = json.load(read_job)

add_new_vac(vacancies, read_job)
try:
    max_salary(int(input("Введите желаемую сумму: ")))
except:
    ValueError: print("Нужно ввести число!")
