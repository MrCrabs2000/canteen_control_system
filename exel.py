from openpyxl import Workbook
from pathlib import Path
from datetime import datetime
from datebase.classes import Product, Dish, Menu, db
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


def export_dishes():
    dishes = db.session.query(Dish).all()

    wb = Workbook()
    ws = wb.active
    ws.title = "Блюда"

    ws['A1'] = 'Название'
    ws['B1'] = 'Категория'
    ws['C1'] = 'Готово на даннный момент'
    ws['D1'] = 'Приготовлено за всё время'
    ws['E1'] = 'Выдано за всё время'

    row = 2

    for dish in dishes:
        if dish.cook_amount > 0:
            ws[f'A{row}'] = dish.name
            ws[f'B{row}'] = dish.category
            ws[f'C{row}'] = dish.amount
            ws[f'D{row}'] = dish.cook_amount
            ws[f'E{row}'] = dish.give_amount
            row += 1

    os.makedirs('exel', exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filepath = Path('exel') / f"dishes_export_{timestamp}.xlsx"
    filepath = filepath.resolve()
    filepath.parent.mkdir(parents=True, exist_ok=True)

    wb.save(str(filepath))
    return filepath


def export_menus():
    menus = db.session.query(Menu).all()

    wb = Workbook()
    ws = wb.active
    ws.title = "Меню"

    ws['A1'] = 'Дата'
    ws['B1'] = 'Тип'
    ws['C1'] = 'Выдано'
    ws['D1'] = 'Цена'
    ws['E1'] = 'Прибыль'

    row = 2

    for menu in menus:
        if menu.get_amount > 0:
            ws[f'A{row}'] = menu.data
            ws[f'B{row}'] = menu.type
            ws[f'C{row}'] = menu.get_amount
            ws[f'D{row}'] = menu.price
            ws[f'E{row}'] = menu.price * menu.get_amount
            row += 1

    os.makedirs('exel', exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filepath = Path('exel') / f"menus_export_{timestamp}.xlsx"
    filepath = filepath.resolve()
    filepath.parent.mkdir(parents=True, exist_ok=True)

    wb.save(str(filepath))
    return filepath