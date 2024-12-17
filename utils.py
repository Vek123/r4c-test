from io import BytesIO
from typing import List, Any, Dict, Tuple

import openpyxl
from django.core.mail import send_mail
from django.conf import settings


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


def send_email(to_email: str, subject: str, message: str):
    send_mail(
        subject,
        message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[to_email],
        auth_user=settings.EMAIL_HOST_USER,
        auth_password=settings.EMAIL_HOST_PASSWORD,
        fail_silently=True,
    )
