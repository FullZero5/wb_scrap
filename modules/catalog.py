import requests
from modules.logger import setup_logger

logger = setup_logger('catalog')

def get_catalogs_wb() -> dict:
    """получаем полный каталог Wildberries"""
    url = 'https://static-basket-01.wbbasket.ru/vol0/data/main-menu-ru-ru-v3.json'
    headers = {'Accept': '*/*', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    return requests.get(url, headers=headers).json()

def get_data_category(catalogs_wb: dict) -> list:
    """сбор данных категорий из каталога Wildberries"""
    catalog_data = []
    stack = [catalogs_wb]
    while stack:
        item = stack.pop()
        if isinstance(item, dict):
            catalog_data.append({
                'name': item.get('name', ''),
                'shard': item.get('shard', None),
                'url': item.get('url', ''),
                'query': item.get('query', None)
            })
            if 'childs' in item:
                stack.extend(item['childs'])
        elif isinstance(item, list):
            stack.extend(item)
    return catalog_data

def search_category_in_catalog(url: str, catalog_list: list) -> dict:
    """проверка пользовательской ссылки на наличии в каталоге"""
    for catalog in catalog_list:
        if catalog['url'] == url.split('https://www.wildberries.ru')[-1]:
            logger.info(f'найдено совпадение: {catalog["name"]}')
            return catalog