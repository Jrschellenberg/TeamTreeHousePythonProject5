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
        print(f"Date String is! {date_string}")
        if date_string == '':
            print("hitting this shit?!")
            date_string = datetime.datetime.now().strftime('%Y-%m-%d')
        return datetime.datetime.strptime(date_string, '%Y-%m-%d').strftime(format_date)

    @classmethod
    # Inspired from https://stackoverflow.com/questions/51094181/convert-integer-to-hours-and-minutes/51094317
    def format_minutes(cls, minutes_integer):
        hours = minutes_integer // 60  # Truncating integer division
        minutes = minutes_integer % 60  # Modulo removes the upper digits

        return_string = ""
        if hours != 0:
            return_string += f'{hours} hour{"s" if hours > 0 else ""}{", " if minutes > 0 else ""}'
        if minutes != 0:
            return_string += f'{minutes} minute{"s" if minutes > 0 else ""}'

        return return_string
