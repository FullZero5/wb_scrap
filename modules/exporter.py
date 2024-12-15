from modules.logger import setup_logger
import pandas as pd
import os

# Настройка логгера для этого модуля
logger = setup_logger('exporter')

def save_excel(data: list, filename: str):
    """
    Сохранение результата в Excel-файл с применением стилей.
    Файл будет сохранен в папку output/.
    """
    # Создаем папку для выходных файлов, если она не существует
    if not os.path.exists('output'):
        os.makedirs('output')
    
    # Создаем DataFrame из данных
    df = pd.DataFrame(data)
    
    # Используем контекстный менеджер для записи в Excel
    with pd.ExcelWriter(f'output/{filename}.xlsx', engine='xlsxwriter') as writer:
        # Записываем данные в лист
        df.to_excel(writer, sheet_name='data', index=False)
        
        # Получаем объект рабочей книги и листа
        workbook = writer.book
        worksheet = writer.sheets['data']
        
        # Создаем стили
        header_format = workbook.add_format({
            'bold': True,  # Жирный текст
            'align': 'center',  # Выравнивание по центру
            'valign': 'vcenter',  # Выравнивание по вертикали по центру
            'bg_color': '#D9E1F2',  # Цвет фона заголовков
            'border': 1  # Границы
        })
        
        cell_format = workbook.add_format({
            'align': 'left',  # Выравнивание по левому краю
            'valign': 'vcenter',  # Выравнивание по вертикали по центру
            'border': 1  # Границы
        })
        
        # Применяем стиль к заголовкам
        for col_num, value in enumerate(df.columns):
            worksheet.write(0, col_num, value, header_format)
        
        # Применяем стиль к данным
        for row_num in range(1, len(df) + 1):
            for col_num in range(len(df.columns)):
                worksheet.write(row_num, col_num, df.iat[row_num - 1, col_num], cell_format)
        
        # Автоматически задаем ширину столбцов
        for idx, column in enumerate(df.columns):
            column_length = max(df[column].astype(str).map(len).max(), len(str(column)))
            worksheet.set_column(idx, idx, column_length + 2)  # +2 для отступов
    
    logger.info(f'Все сохранено в output/{filename}.xlsx\n')