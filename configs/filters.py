from flask import Flask
from datetime import date


def register_filters(app: Flask):
    app.jinja_env.filters['date_fM_d'] = date_fM_d
    app.jinja_env.filters['date_Y_M_d'] = date_Y_M_d


def date_fM_d(date: date):
    formated_date = ''

    try:
        formated_date = date.strftime('%-d %B')
    except: 
        formated_date = date.strftime('%#d %B')

    return formated_date


def date_Y_M_d(date: date):
    formated_date = ''

    try:
        formated_date = date.strftime('%-d.%m.%Y')
    except: 
        formated_date = date.strftime('%#d.%m.%Y')

    return formated_date
    