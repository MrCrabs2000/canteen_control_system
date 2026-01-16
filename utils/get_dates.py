from datetime import date, timedelta


def get_dates(delta_past, delta_future):
    start = date.today() - timedelta(days=delta_past)
    
    dates = list()
    prev_date = start

    for i in range(delta_past + delta_future + 1):
        dates.append(prev_date)
        prev_date = prev_date + timedelta(days=1)

    return dates