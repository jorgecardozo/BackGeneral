import re

def recursive_parse_dict(field, value, _dict):
    pattern = re.compile(r'(?P<field>.*?)[\[](?P<subfield>.*?)[\]](?P<extra>.*?)$')
    matcher = pattern.match(field)
    data = matcher.groupdict() if not matcher == None else { "field": field, "extra": None }
    
    if data['extra'] != None:
        field = data['field']
        subfield = data['subfield']
        if not field in _dict:
            _dict[field] = {}
        if data['extra'] != '':
            _field = subfield + data['extra']
            recursive_parse_dict(_field, value, _dict[field])
        else:
            _dict[field][subfield] = value
    else:
        _dict[field] = value

def array_is_numeric(_array):
    for v in _array:
        if type(v) != int and type(v) != float and (type(v) == str and not v.isdigit()):
            return False
    return True

def recursive_convert_dict_to_array(_dict):
    for key, value in _dict.items():
        if type(value) == dict:
            recursive_convert_dict_to_array(_dict[key])
            if array_is_numeric(value.keys()):
                _dict[key] = [v for k, v in value.items()]

def FormData(data):
    reply = {}
    try:
        for field, value in data.items():
            recursive_parse_dict(field, value, reply)
        recursive_convert_dict_to_array(reply)
    except Exception as ex:
        print(ex)
    return reply