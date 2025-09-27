from datetime import datetime as dt


class DateConverter:
    regex = r'\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        return dt.strptime(value, '%Y-%m-%d').date()

    def to_url(self, value):
        return value.strftime('%Y-%m-%d')
