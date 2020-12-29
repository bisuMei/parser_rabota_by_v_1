import urllib.parse

import requests
from bs4 import BeautifulSoup
import csv
import dateparser
import lxml


CSV = 'vacancies.csv'
# домен который мы парсим
HOST = 'https://rabota.by/'

URL = 'https://rabota.by/search/vacancy?clusters=true&area=1002&enable_snippets=true&salary=&st=searchVacancy&text=Python+%D1%80%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D1%87%D0%B8%D0%BA&from=suggest_post'

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html_):
    soup = BeautifulSoup(html_, 'html.parser')
    items = soup.find_all('div', class_='vacancy-serp-item')
    vacancies = []

    for item in items:
        post_date = item.select_one('span.vacancy-serp-item__publication-date').get_text('\n')
        absolute_date = dateparser.parse(post_date, date_formats=['%H:%M', ])
        vacancies.append(
            {
                'title': item.select_one('span.g-user-content').string.strip(),
                'vacancy_link': item.find('a', class_='bloko-link').get('href'),
                'company': item.select_one('div.vacancy-serp-item__meta-info-company').string.strip(),
                'post_date': absolute_date,

            }
        )
    return vacancies


def get_pagination_limit():
    text = get_html(URL)

    soup = BeautifulSoup(text.text, 'lxml')

    container = soup.select('a.bloko-button.HH-Pager-Control')

    limit_list = []

    for item in container:
        x = item.text
        limit_list.append(x)

    last_button = limit_list[-2]

    return int(last_button)


def save_to_csv(items, path):
    with open(path, 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['Title', 'Link', 'Company', 'Date'])
        for item in items:
            writer.writerow([item['title'], item['vacancy_link'], item['company'], item['post_date']])


def parse_all():
    # pagination = int(input('How much pages you want to parse?: '))
    pagination = get_pagination_limit()
    html_ = get_html(URL)
    if html_.status_code == 200:
        vacancies = []
        for page in range(0, pagination):
            print("Parsing page {}".format(page))
            html_ = get_html(URL, params={'page': page})
            vacancies.extend(get_content(html_.text))
            save_to_csv(vacancies, CSV)

    else:
        print("Error")


parse_all()



