import datetime

def date():
    now = datetime.datetime.now()
    dateNow = now.date().strftime('%d.%m.%Y')
    return  dateNow