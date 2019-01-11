from django.db.models import Func, CharField, FloatField, Aggregate
from django.db import connection

class LPAD(Func):
    function = 'LPAD'
    template = "%(function)s(%(expressions)s, %(Length)s, %(Char)s)"
    if connection.vendor == 'sqlite':
        function = 'substr'
        template = "%(function)s('%(pad_str)s' || %(expressions)s, length('%(pad_str)s' || %(expressions)s) - (%(Length)s - 1), %(Length)s)"
    elif connection.vendor == 'postgresql':
        function = 'LPAD'
        template = "%(function)s(%(expressions)s::text, %(Length)s, '%(Char)s')"
    def __init__(self, expression, Length = 1, Char = '0', **extra):
        pad_str = ""
        for i in range(0, Length):
            pad_str += Char
        super(LPAD, self).__init__(
            expression,
            Length = Length,
            Char = Char,
            pad_str = pad_str,
            output_field = CharField(),
            **extra)
    
class Round(Func):
    function = 'ROUND'
    template = '%(function)s(%(expressions)s, %(Length)s)'
    if connection.vendor == 'postgresql':
        template = '%(function)s(%(expressions)s::numeric, %(Length)s)'
    
    def __init__(self, expression, Length = 2, **extra):
        super(Round, self).__init__(
            expression,
            Length = Length,
            output_field = FloatField(),
            **extra
        )