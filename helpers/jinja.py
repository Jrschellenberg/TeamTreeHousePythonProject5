import datetime
from inspect import getmembers, ismethod


class JinjaHelpers:
    def __init__(self, app):
        self.app = app

    def register(self):
        for key, val in getmembers(self, predicate=ismethod):
            if key is 'register' or key is '__init__':
                continue
            print(f"registering {key} {val}")
            self.app.jinja_env.filters[key] = val

    @classmethod
    def date_format(cls, date_string, format_date='%Y-%m-%d'):
        if date_string == '':
            date_string = datetime.datetime.now().strftime('%Y-%m-%d')
        return datetime.datetime.strptime(date_string, '%Y-%m-%d').strftime(format_date)
