import logging
import os

def setup_logger(name):
    """
    Настройка логгера для конкретного модуля.
    Логи будут сохраняться в папку logs/.
    """
    # Создаем папку для логов, если она не существует
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Создаем обработчик для записи в файл
    file_handler = logging.FileHandler('logs/parser.log', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    # Создаем форматтер и добавляем его в обработчик
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    # Добавляем обработчик в логгер
    logger.addHandler(file_handler)
    
    # Добавляем обработчик для вывода в консоль
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger