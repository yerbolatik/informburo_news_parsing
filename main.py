import re
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def get_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении {url}: {e}")
        return None


def parse_article(article_url, driver):
    driver.get(article_url)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'h1')))
    except Exception as e:
        print(f"Не удалось загрузить статью: {article_url}")
        print(e)
        return None

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    title = soup.find('h1').text.strip() if soup.find('h1') else ''
    post_time_elem = soup.find('time')
    post_time = post_time_elem['datetime'].strip() if post_time_elem else ''

    views_elem = soup.find('small', id=re.compile(
        r'arrilot-widget-container-\d+'))
    if views_elem:
        views_text = views_elem.text.strip()
        views_match = re.search(r'\d+', views_text)
        views_number = views_match.group() if views_match else ''
    else:
        views_number = ''

    image_elem = soup.find('img', class_='article-img')
    image_url = 'https://informburo.kz' + \
        image_elem['src'] if image_elem and 'src' in image_elem.attrs else ''

    text_elem = soup.find('div', class_='article')
    text = ''.join(p.text for p in text_elem.find_all('p')
                   ).strip() if text_elem else ''

    tags_elem = soup.find('ul', class_='article-tags')
    tags = [tag.text.strip()
            for tag in tags_elem.find_all('a')] if tags_elem else []

    return {
        'title': title,
        'text': text,
        'post_time': post_time,
        'tags': tags,
        'views': views_number,
        'image_url': image_url,
        'url': article_url
    }


def parse_page(url, driver):
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class*="uk-width-2-3"] ul.uk-nav-default > li.uk-grid')))
    except Exception as e:
        print(f"Не удалось загрузить страницу: {url}")
        print(e)
        with open(f"error_page_{url.split('=')[-1]}.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        return []

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    articles = soup.select(
        'div[class*="uk-width-2-3"] ul.uk-nav-default > li.uk-grid')

    data = []

    for article in articles:
        url_element = article.select_one('div.uk-width-expand a')
        if url_element:
            article_url = url_element['href']
            if not article_url.startswith('https://'):
                article_url = 'https://informburo.kz' + article_url
            article_data = parse_article(article_url, driver)
            if article_data:
                data.append(article_data)
        else:
            print("Ошибка: Не удалось найти элемент URL статьи")

    return data


def main():
    base_url = 'https://informburo.kz/novosti?page='
    all_data = []

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)

    try:
        for page in range(1, 101):
            url = base_url + str(page)
            print(f'Парсинг страницы {page}')
            driver.delete_all_cookies()  # Очистка cookies перед каждой страницей
            page_data = parse_page(url, driver)
            all_data.extend(page_data)
            time.sleep(5)  # Увеличиваем задержку между запросами
    finally:
        driver.quit()

    df = pd.DataFrame(all_data)
    df.to_csv('informburo_news.csv', index=False, encoding='utf-8-sig')


if __name__ == '__main__':
    main()
