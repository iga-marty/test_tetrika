from typing import Optional

import csv
import requests
from bs4 import BeautifulSoup


base_url = 'https://ru.wikipedia.org'
next_url = '/wiki/Категория:Животные_по_алфавиту'
letters_count = {}

def parser(url: str) -> Optional[str]:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')

    mw_pages = soup.find(name='div', id='mw-pages')
    mw_groups = mw_pages.find_all(name='div', class_='mw-category-group')

    for group in mw_groups:
        letter = group.find(name='h3').text
        if letter == 'A':
            return None
        count = len(group.find_all(name='li'))
        # print(letter, count)
        existing_count = letters_count.get(letter)
        letters_count[letter] = count + existing_count if existing_count is not None else count
        # print(letters_count)
    next_url = soup.find('a', string='Следующая страница').get('href')
    return next_url

def save_to_csv(data, filename='beasts.csv'):
    with open(filename, 'w', newline='', errors='ignore', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(data)

if __name__ == '__main__':
    while next_url is not None:
        url = base_url + next_url
        next_url = parser(url)
        print(letters_count)

    save_to_csv(letters_count.items())

