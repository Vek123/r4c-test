from io import BytesIO
from typing import List, Any, Dict, Tuple

import openpyxl


def create_excel_file(headers: Tuple, data: Dict[Any, List[Any]]) -> BytesIO:
    """
    :param headers: Первая строка в файле (названия столбцов)
    :param data: Данные в формате {`название листа`: `список строк`}
    :return: BytesIO - Каретка в начале
    """
    virtual_file = BytesIO()
    excel_file = openpyxl.Workbook()
    excel_file.remove_sheet(excel_file.worksheets[0])
    for sheet_name in data:
        sheet = excel_file.create_sheet(sheet_name)
        sheet.append(headers)
        for row in data[sheet_name]:
            sheet.append(row)
    excel_file.save(virtual_file)
    virtual_file.seek(0)

    return virtual_file
