from django.db.models import Func, CharField, FloatField, Aggregate
from django.db import connection


class GroupConcat(Aggregate):
    function = 'string_agg'
    template='%(function)s(%(expressions)s, \' %(separator)s \')'

    if connection.vendor == 'sqlite':
        function = 'GROUP_CONCAT'

    def __init__(self, expression, separator = ',', **extra):
        super(GroupConcat, self).__init__(
            expression,
            separator = separator,
            output_field=CharField(),
            **extra
        )