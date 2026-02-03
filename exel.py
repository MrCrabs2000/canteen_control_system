from openpyxl import Workbook
from pathlib import Path
from datetime import datetime
from datebase.classes import Product, db
import os


def export_products():
    products = db.session.query(Product).all()

    wb = Workbook()
    ws = wb.active
    ws.title = "Продукты"

    ws['A1'] = 'Название'
    ws['B1'] = 'Куплено'
    ws['C1'] = 'Потрачено'
    ws['D1'] = 'Единица'

    row = 2

    for product in products:
        if product.buy_amount > 0:
            ws[f'A{row}'] = product.name
            ws[f'B{row}'] = product.buy_amount
            ws[f'C{row}'] = product.spend_amount
            ws[f'D{row}'] = product.measurement
            row += 1

    os.makedirs('exel', exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filepath = Path('exel') / f"products_export_{timestamp}.xlsx"
    filepath = filepath.resolve()
    filepath.parent.mkdir(parents=True, exist_ok=True)

    wb.save(str(filepath))
    return filepath