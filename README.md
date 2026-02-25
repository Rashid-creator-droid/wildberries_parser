# Парсер Wildberries
# Стек технологий
<div id="badges" align="center">
  <img src="https://img.shields.io/badge/Python%203.12-FFD43B?style=for-the-badge&logo=python&logoColor=blue"/>

</div>

# Описание проекта
Парсер Wildberries предназначен для асинхронного сбора информации о товарах с сайта Wildberries с возможностью применения фильтров по рейтингу, цене и стране происхождения.
### Особенности.
На данный момент реализовано:
- Асинхронный сбор данных с использованием httpx и asyncio.
- Поддержка фильтров по:
  - Рейтингу (rating_min, rating_max)
  - Цене (price_min, price_max)
  - Стране производителя (country)
- Возможность ограничения количества страниц (limit_pages) и количества товаров на странице (limit_per_page).
- Автоматическая запись результатов в Excel с поддержкой пакетной записи.
- Настройки запросов, заголовков и URL задаются через конфигурационный файл [config.json](config.json).
- Поддержка использования cookie и прокси через .env.

## Установка проекта из репозитория GitHub.
### Установить Python 3.12
- Для Windows https://www.python.org/downloads/
- Для Linux 
```bash
    sudo apt update
    sudo apt -y install python3-pip
    sudo apt install python3.12
``` 
### Клонировать репозиторий и перейти в него в командной строке.
```bash
  git clone https://github.com/Rashid-creator-droid/wildberries_parser.git
``` 
###  Развернуть виртуальное окружение.
```bash
  python -m venv venv
``` 
 - для Windows;
```bash
  .\.venv\Scripts\Activate.ps1 
``` 
 - для Linux и MacOS.
``` bash
    source venv/bin/activate
```
### Установить систему контроля зависимостей Poetry
```bash
    pip install poetry
``` 
### Установить зависимости
```bash
    poetry install
```
### Создать файл .env с необходимыми параметрами в корне проекта:
```env
    WB_COOKIE=ваш_cookie_сайт
    PROXY_URL=ваш_proxy_адрес
```
### Запуск.
Запуск без аргументов.
```bash
    python main.py
```
### Запуск с аргументами:
 - Количество продуктов на странице --limit-per-page
 - Количество страниц --limit-pages 
 - Исользовать фильтры --use-filters

Пример
```bash
    python main.py --limit-per-page 87 --limit-pages 3 --use-filters
```
## Настройка конфигурации.

Конфигурация парсера задается в [config.json](config.json), здесь задаются параметры headers, params, urls, а также параметры фильтров, для парсинга по фильтрам.
Доступны фильтры по рейтингу (rating_min - нижняя граница рейтинга, rating_max - верхняя граница рейтинга), цене (price_min, price_max) и стране (доступны страны: RUSSIA, BELARUS, CHINA, KYRGYZSTAN, TURKEY, UK, VIETNAM, ITALY, FINLAND)
```json
    {
  "base_url": "https://www.wildberries.ru/",
  "products_api_url": "__internal/u-search/exactmatch/ru/common/v18/search",
  "product_url_template": "catalog/{product_id}/detail.aspx",
  "product_base_api_template": "https://basket-{basket_id}.wbbasket.ru/vol{vol}/part{part}/{product_id}/",
  "product_api_prefix": "info/ru/card.json",
  "image_url_prefix": "images/big/{image_number}.webp",
  "seller_url_prefix": "seller/{supplier_id}",
  "seller_url_template": "https://static-basket-01.wbbasket.ru/vol0/data/supplier-by-id/{supplier_id}.json",

  "search": {
    "query": "пальто из натуральной шерсти"
  },

  "filters": {
    "rating_min": 4.5,
    "rating_max": 5,
    "price_min": 0,
    "price_max": 10000,
    "country": "RUSSIA"
  },

  "request": {
    "params": {
      "resultset": "catalog",
      "sort": "popular",
      "lang": "ru",
      "curr": "rub",
      "dest": "-2133462"
    },
    "headers": {
      "user-agent": "Mozilla/5.0",
      "accept": "application/json",
      "accept-language": "ru"
    }
  }
}
```
## Запись в файл XLSX.
Результаты сохраняются в Excel. Имя файла формируется автоматически на основе запроса и фильтров. Если файл с таким именем уже существует, к имени добавляется номер _1, _2 и так далее.