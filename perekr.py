import requests
from bs4 import BeautifulSoup
import os
import csv
import json
from time import sleep
import random

try:
    os.mkdir('Data')
except FileExistsError:
    pass

url = 'https://www.perekrestok.ru/cat'

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
}

req = requests.get(url, headers=headers)
src = req.text

with open('index.html', 'w') as f:
    f.write(src)

with open('index.html') as f:
    src = f.read()

soup = BeautifulSoup(src, 'lxml')

all_groups = soup.find_all(class_="sc-dlfnbm jwhrZg")

# Перебираем все группы с гравной страницы
for group in all_groups:
    group_name = group.find(class_="category-card__title").text
    rep = [' ', '-', ',', '/']
    for symbol in rep:
        if symbol in group_name:
            group_name = group_name.replace(symbol, '_')
    if '__' in group_name:
        group_name = group_name.replace('__', '_')
    group_href = 'https://www.perekrestok.ru' + group.find(class_="sc-jSgupP bnmesn").get('href')

    try:
        os.mkdir(f'Data//{group_name}')
    except FileExistsError:
        pass

    req = requests.get(group_href, headers=headers)
    src = req.text

    print(f'### Пишем {group_name} ###')

    with open(f'Data//{group_name}.html', 'w') as f:
        f.write(src)

    with open(f'Data//{group_name}.html') as f:
        src = f.read()

    soup = BeautifulSoup(src, 'lxml')
    all_subgroups = soup.find(class_="category-filter-item__content").find_all('a')
    # print(all_subgroups)
    for subgroup in all_subgroups:
        subgroup_name = subgroup.text
        rep = [' ', '-', ',', '/']
        for symbol in rep:
            if symbol in subgroup_name:
                subgroup_name = subgroup_name.replace(symbol, '_')
        if '__' in subgroup_name:
            subgroup_name = subgroup_name.replace('__', '_')
        subgroup_href = 'https://www.perekrestok.ru' + subgroup.get('href')

        req = requests.get(subgroup_href, 'lxml')
        src = req.text

        print(f'# Пишем {subgroup_name} #')
        with open(f'Data/{group_name}/{subgroup_name}.html', 'w') as f:
            f.write(src)

        with open(f'Data/{group_name}/{subgroup_name}.html') as f:
            src = f.read()

        with open(f'Data/{group_name}/{subgroup_name}.csv', 'w', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(
                (
                    'Продукт',
                    'Цена старая',
                    'Цена новая',
                    'Скидка',
                    'Ссылка'
                )
            )

        product_info = []

        soup = BeautifulSoup(src, 'lxml')
        all_products = soup.find_all(class_="sc-dlfnbm ldVxnE")

        for product in all_products:
            # Название продукта
            if product.find(class_="product-card__title") != None:
                name = product.find(class_="product-card__title").text
            else:
                name = '-'
            # Цена старая
            if product.find(class_="price-old") != None:
                price_old = product.find(class_="price-old").text
            else:
                price_old = '-'
            # Цена новая
            if product.find(class_="price-new") != None:
                price_new = product.find(class_="price-new").text
            else:
                price_new = '-'
            # Скидка на продукт
            if product.find(class_="sc-jcVebW ekWoFb product-card__badge") != None:
                badge = product.find(class_="sc-jcVebW ekWoFb product-card__badge").text
            else:
                badge = '-'
            # Ссылка на продукт
            if product.find(class_="sc-jSgupP bnmesn product-card__link") != None:
                link = 'https://www.perekrestok.ru' + product.find(class_="sc-jSgupP bnmesn product-card__link").get('href')
            else:
                link = '-'

            with open(f'Data/{group_name}/{subgroup_name}.csv', 'a', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(
                    (
                        name,
                        price_old,
                        price_new,
                        badge,
                        link
                    )
                )

            product_info.append(
                {
                    'name': name,
                    'price_old': price_old,
                    'price_new': price_new,
                    'badge': badge,
                    'link': link
                }
            )
        with open(f'Data/{group_name}/{subgroup_name}.json', 'w', encoding='utf-8') as f:
            json.dump(product_info, f, indent=4, ensure_ascii=False)

        sleep(random.randrange(1, 10))
    sleep(random.randrange(1, 10))
