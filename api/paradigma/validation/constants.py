MessageErrorCodes = {
    'null':"El campo no puede ser nulo.",
    'blank':"El campo no puede estar vacio.",
    'required':"El campo es requerido.",
    'invalid':"El campo es invalido.",
    'NOT_STRING':"El campo debe ser un string.",
    'NOT_INTEGER':"El campo debe ser un integer.",
    'NOT_BOOLEAN':"El campo debe ser un booleano.",
    'max_length':"El campo es demasiado largo.",
    'min_length':"El campo es demasiado corto.",
    'unique':"Ya existe un registro con este valor.",
    'empty':"El campo no puede estar vacio.",
    'does_not_exist': "No existe un registro con este ID.",
    'not_a_list': "No es una lista."
}

class ErrorCodes:
    code = ''
    detail = ''

    def __init__(self, code, detail):
        self.code = code
        self.detail = detail

NotFound = ErrorCodes('not_found',"El objeto con id '%s' no fue encontrado.")
