from modules.logger import setup_logger
from modules.catalog import get_catalogs_wb, get_data_category, search_category_in_catalog
from modules.scraper import scrap_page, get_data_from_json
from modules.exporter import save_excel

# Настройка логгера для основного модуля
logger = setup_logger('main')

def parser(url: str, low_price: int = 1, top_price: int = 1000000, discount: int = 0):
    """основная функция"""
    catalog_data = get_data_category(get_catalogs_wb())
    try:
        category = search_category_in_catalog(url=url, catalog_list=catalog_data)
        data_list = []
        for page in range(1, 51):
            data = scrap_page(
                page=page,
                shard=category['shard'],
                query=category['query'],
                low_price=low_price,
                top_price=top_price,
                discount=discount)
            logger.info(f'Добавлено позиций: {len(get_data_from_json(data))}')
            if len(get_data_from_json(data)) > 0:
                data_list.extend(get_data_from_json(data))
            else:
                break
        logger.info(f'Сбор данных завершен. Собрано: {len(data_list)} товаров.')
        if not data_list:
            logger.warning('Внимание: нет данных для сохранения.')
            return
        save_excel(data_list, f'{category["name"]}_from_{low_price}_to_{top_price}')
        logger.info(f'Ссылка для проверки: {url}?priceU={low_price * 100};{top_price * 100}&discount={discount}')
    except TypeError:
        logger.critical('Ошибка! Возможно не верно указан раздел. Удалите все доп фильтры с ссылки')
    except PermissionError:
        logger.critical('Ошибка! Вы забыли закрыть созданный ранее excel файл. Закройте и повторите попытку')
    except KeyError:
        logger.critical('Ошибка! Не найдены ключи в данных категории.')
    except Exception as e:
        logger.critical(f'Неизвестная ошибка: {e}')

if __name__ == '__main__':
    while True:
        url = input('Введите ссылку на категорию без фильтров для сбора (или "q" для выхода):\n')
        if url.lower() in ('q', 'exit'):
            break
        try:
            low_price = int(input('Введите минимальную сумму товара: '))
            top_price = int(input('Введите максимальную сумму товара: '))
            discount = int(input('Введите минимальную скидку (введите 0 если без скидки): '))
            parser(url=url, low_price=low_price, top_price=top_price, discount=discount)
        except ValueError:
            logger.critical('Ошибка! Проверьте правильность введенных данных.')