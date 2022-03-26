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
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
    "cookie": '_gcl_au=1.1.900861375.1644765567; tmr_lvid=aeb76cab3153cd28bca1a01d0dc5bc41; tmr_lvidTS=1644765567621; _ym_uid=1644765568844451382; _ym_d=1644765568; _fbp=fb.1.1644765567860.639205379; agreements=j:{"isCookieAccepted":true,"isAdultContentEnabled":true,"isAppAppInstallPromptClosed":false}; flocktory-uuid=3cd8c6ab-99a4-4e41-8163-fcb5ee2e70e4-5; _ym_isad=2; _gid=GA1.2.2119018397.1647786493; coords=j:[37.5902646,54.1832091]; _ga=GA1.2.719832659.1644765568; tmr_detect=0%7C1647791209979; session=j:{"accessToken":"eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzUxMiJ9.eyJpYXQiOjE2NDc3ODY0OTAsImV4cCI6MTY0NzgxNTI5MCwiZCI6IjEuNC4xLjA6ZjQzYTYwYTctMmYyNC00MmQwLTljYjItZmM3OTE3MWI0ZjJlIiwianRpIjoiZTM0NjA5MmEtNDVhZS00MDVjLWE4ZTEtZDkxOWI4ZWY5N2JiIiwiaXAiOiI4MC44MC4xOTQuMjM5IiwidSI6ImEzNjg0NDYyLWY3ZjQtNDI3Zi05YmQxLTliYjM2ZTBlOTJiZSJ9.ARQp0DvrGFYKJ60gafKKeA1gbs9nr7KQvwak7j5E_zZXzzS7qBPO2JmNHpmhB6IS5_6kRJc10NrvDPkmpRvkYrtHAZBDsrqNlasqgji7BufkwYVyPssAcapMuHqdIfOYv5ckP0P0TvNMWX3L6T3GiBJHM0FcJoMirsk7cwWg5CgwslHX","refreshToken":"eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzUxMiJ9.eyJpYXQiOjE2NDc3ODY0OTAsImV4cCI6MTY2MzMzODQ5MCwiZCI6IjEuNC4xLjA6ZjQzYTYwYTctMmYyNC00MmQwLTljYjItZmM3OTE3MWI0ZjJlIiwianRpIjoiMDQyZjA5MDUtMzk3Yy00ZTBkLTgyMjAtNzZlMTAwNTBhZDcwIiwiaXAiOiI4MC44MC4xOTQuMjM5IiwidSI6ImEzNjg0NDYyLWY3ZjQtNDI3Zi05YmQxLTliYjM2ZTBlOTJiZSJ9.AevGCJiTwTBMc5ze1-oqRPtm2m7qRWrI3_LpRWteBlWwq97zy0-mJpf7l9VfxxZdiDZaXmnNOYuHQjL_kTTuF5a-AS47LyX3v_lmDp3erz7wLnUID65c5FNMeYhSOhAUFVAImX78C_2C85vpbD1_g3lw1R82Ngd98xmX-AVylq0wjTng","accessTokenExpiredAt":1647815290726,"refreshTokenExpiredAt":1663338490738,"device":{"uuid":"f43a60a7-2f24-42d0-9cb2-fc79171b4f2e"}}; tmr_reqNum=262; _dc_gtm_UA-189134493-1=1; TS0115a7cc=01a93f754737cb518f1873f503c428dc820053107b9c48f608afb3c38547d29dee111b6b1a46a3ab5a0df23731f70d22e0c13c57560fd37f728df9b6495a3e8debabfba776; _ga_5K49P5RFR8=GS1.1.1647795005.16.1.1647795419.49'}


def request(url, output_html):
    req = requests.get(url, headers=headers)
    src = req.text

    with open(output_html, 'w') as f:
        f.write(src)

    with open(output_html) as f:
        src = f.read()

    return BeautifulSoup(src, 'lxml')


soup = request(url, 'index.html')

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

    print(f'### Пишем {group_name} ###')

    soup = request(group_href, f'Data//{group_name}.html')

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

        print(f'# Пишем {subgroup_name} #')

        soup = request(subgroup_href, f'Data/{group_name}/{subgroup_name}.html')

        all_products = soup.find_all(class_="sc-dlfnbm ldVxnE")

        product_info = []

        for product in all_products:
            # Название продукта
            try:
                name = product.find(class_="product-card__title").text
            except Exception:
                name = '-'
            # Цена старая
            try:
                price_old = product.find(class_="price-old").text
            except Exception:
                price_old = '-'
            # Цена новая
            try:
                price_new = product.find(class_="price-new").text
            except Exception:
                price_new = '-'
            # Скидка на продукт
            try:
                badge = product.find(class_="product-card__badges").find('span').text
            except Exception:
                badge = '-'
            # Ссылка на продукт
            try:
                link = 'https://www.perekrestok.ru' + product.find(class_="sc-jSgupP bnmesn product-card__link").get('href')
            except Exception:
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
