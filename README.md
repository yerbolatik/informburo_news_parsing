````markdown
# Парсер новостей с сайта Informburo.kz

Этот проект представляет собой скрипт на Python для парсинга новостей с сайта Informburo.kz и сохранения их в CSV файле.

## Установка зависимостей

Для установки необходимых зависимостей выполните следующие шаги:

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/yerbolatik/informburo_news_parsing.git
   ```
````

2. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

## Использование

1. Запустите скрипт `main.py`, чтобы начать парсинг новостей с сайта Informburo.kz:

   ```bash
   python main.py
   ```

2. Данные будут сохранены в CSV файл `informburo_news.csv`.

## Описание файлов

- `main.py`: Основной скрипт для запуска парсера.
- `requirements.txt`: Файл с перечислением зависимостей проекта.

## Зависимости

- `requests`: Для выполнения HTTP запросов.
- `beautifulsoup4`: Для парсинга HTML контента.
- `selenium`: Для автоматизации веб-браузера.
- `webdriver-manager`: Для управления драйверами браузера.
- `pandas`: Для работы с данными в формате DataFrame и сохранения в CSV.

```

```