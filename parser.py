# parser.py
import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
import time

def parse_kivano(query: str, max_pages=2):
    base_url = "https://www.kivano.kg"
    search_url = f"{base_url}/product/index?search={urllib.parse.quote(query)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    products = []
    session = requests.Session()

    for page in range(1, max_pages + 1):
        url = search_url + (f"&page={page}" if page > 1 else "")
        try:
            response = session.get(url, headers=headers)
            response.raise_for_status()
        except Exception as e:
            print(f"Ошибка при загрузке страницы {page}: {e}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.select('div.item.product_listbox.oh')

        if not items:
            break

        for item in items:
            try:
                title_tag = item.select_one('div.listbox_title a')
                price_tag = item.select_one('div.listbox_price')
                img_tag = item.select_one('img')

                if not title_tag or not price_tag or not img_tag:
                    continue

                name = title_tag.get_text(strip=True)
                price_text = price_tag.get_text(strip=True)
                price = ''.join(filter(str.isdigit, price_text))

                link = base_url + title_tag['href']
                img_src = img_tag.get('src') or img_tag.get('data-src')
                if img_src and not img_src.startswith('http'):
                    img_url = base_url + img_src
                else:
                    img_url = img_src

                products.append({
                    "Название": name,
                    "Цена (сом)": price,
                    "Ссылка": link,
                    "Изображение": img_url
                })
            except Exception as e:
                continue

        time.sleep(1.5)

    return products