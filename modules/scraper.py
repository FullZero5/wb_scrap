import requests
from retry import retry
from modules.logger import setup_logger

logger = setup_logger('scraper')

@retry(Exception, tries=5, delay=2)
def scrap_page(page: int, shard: str, query: str, low_price: int, top_price: int, discount: int = None) -> dict:
    """Сбор данных со страниц"""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0)"}
    url = f'https://catalog.wb.ru/catalog/{shard}/catalog?appType=1&curr=rub' \
          f'&dest=-1257786' \
          f'&locale=ru' \
          f'&page={page}' \
          f'&priceU={low_price * 100};{top_price * 100}' \
          f'&sort=popular&spp=0' \
          f'&{query}' \
          f'&discount={discount}'
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        logger.error(f'Ошибка HTTP: {r.status_code}')
        raise Exception(f'Ошибка HTTP: {r.status_code}')
    logger.info(f'Статус: {r.status_code} Страница {page} Идет сбор...')
    return r.json()

def get_data_from_json(json_file: dict) -> list:
    data_list = []
    products = json_file.get('data', {}).get('products', [])
    if not products:
        logger.warning('Внимание: нет данных для обработки.')
    for product in products:
        data_list.append({
            'id': product.get('id'),
            'name': product.get('name'),
            'price': int(product.get('priceU', 0) / 100),
            'salePriceU': int(product.get('salePriceU', 0) / 100),
            'cashback': product.get('feedbackPoints'),
            'sale': product.get('sale'),
            'brand': product.get('brand'),
            'rating': product.get('rating'),
            'supplier': product.get('supplier'),
            'supplierRating': product.get('supplierRating'),
            'feedbacks': product.get('feedbacks'),
            'reviewRating': product.get('reviewRating'),
            'promoTextCard': product.get('promoTextCard'),
            'promoTextCat': product.get('promoTextCat'),
            'link': f'https://www.wildberries.ru/catalog/{product.get("id")}/detail.aspx?targetUrl=BP'
        })
    return data_list