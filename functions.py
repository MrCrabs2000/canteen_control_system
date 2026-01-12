from json import loads, dumps
from datetime import date, timedelta


def json_to_str(json_text):
    text, a, res = loads(json_text), 1, ''
    for key in text.keys():
        if a == len(text):
            res += text[key]
        else:
            res += text[key] + ' '
            a += 1
    return res


def str_to_json(text):
    text = text.strip().split()
    res = {}
    for i in range(len(text)):
        res[str(i)] = text[i]
    return dumps(res)


def get_dates(delta_past, delta_future):
    start = date.today() - timedelta(days=delta_past)
    
    dates = list()
    prev_date = start

    for i in range(delta_past + delta_future + 1):
        dates.append(prev_date)
        prev_date = prev_date + timedelta(days=1)

    return dates