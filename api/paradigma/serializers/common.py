from rest_framework import status
from rest_framework.response import Response
from django.http.response import JsonResponse
from paradigma.validation.functions import ParseValidationErrors
from paradigma.validation.constants import NotFound

def JsonResult(status, meta = None, data = None, errors = None):
    obj = dict()
    if meta != None:
        obj["meta"] = meta
    if data != None:
        obj["data"] = data
    if errors != None:
        obj["errors"] = errors
    response = Response(obj, status=status)
    return response

def CreatedJsonResult(new_obj, meta = None):
    if meta == None:
        meta = {
            'allowed': True,
        }
    return JsonResult(status.HTTP_201_CREATED, meta, new_obj)

def ValidJsonResultSet(rows=[], 
    int_rows = 0, 
    int_total_rows = 0, 
    int_total_rows_filtered = 0, 
    int_page = 0, 
    int_total_pages = 1, 
    int_page_size = None):
    meta = {
        'rows': int_rows,
        'totalRows': int_total_rows,
        'totalRowsFiltered': int_total_rows_filtered,
        'page': int_page,
        'totalPages': int_total_pages,
        'pageSize': int_page_size,
    }
    return ValidJsonResult(rows, meta)

def ValidJsonResult(data = None, meta = None):
    if meta == None:
        meta = {
            'allowed': True,
        }
    return JsonResult(status.HTTP_200_OK, meta, data)

def InvalidJsonResult(errors, data = None, meta = None):
    if meta == None:
        meta = {
            'allowed': True,
        }
    return JsonResult(status.HTTP_400_BAD_REQUEST, meta, data, errors)

def ValidationErrorJsonResult(errors, data = None, meta = None):
    if meta == None:
        meta = {
            'allowed': True,
        }
    parsed_errors = ParseValidationErrors(errors)
    return JsonResult(status.HTTP_400_BAD_REQUEST, meta, data, parsed_errors)

def NotFoundJsonResult(errors = None, meta = None):
    if meta == None:
        meta = {
            'allowed': True,
        }
    return JsonResult(status.HTTP_404_NOT_FOUND, meta, None, [{'id': errors[0], 'code':NotFound.code, 'detail': NotFound.detail.replace('%s', str(errors[0]))}])

def AuthenticationFailedJsonResult(errors = None, meta = None):
    if meta == None:
        meta = {
            'allowed': True,
        }
    errors = {
        'error': 'El usuario y/o contraseña son incorrectos.'
    }
    return JsonResult(status.HTTP_400_BAD_REQUEST, meta, None, errors)

def UnauthorizedJsonResult(errors = None, meta = None):
    if meta == None:
        meta = {
            'allowed': True,
        }
    meta = {
        'allowed': False,
        'authorization': 'required'
    }
    return JsonResult(status.HTTP_401_UNAUTHORIZED, meta, None, None)


def PermissionJsonResult(errors = None, meta = None):
    if meta != None:
        meta['allowed'] = False
        if 'message' not in meta.keys():
            meta['message'] = "No tiene permisos para realizar esta acción."
    else:
        meta = {
            'allowed': False,
            'message': "No tiene permisos para realizar esta acción."
        }
    return JsonResult(status.HTTP_401_UNAUTHORIZED, meta, None, None)


def ProtectedErrorJsonResult(errors = None, meta = None):
    if meta != None:
        meta['allowed'] = False
        if 'message' not in meta.keys():
            meta['message'] = "La entidad que intenta eliminar se encuentra protegida por otro modelo de base de datos."
    else:
        meta = {
            'allowed': False,
            'protected': True,
            'message': "La entidad que intenta eliminar se encuentra protegida por otro modelo de base de datos."
        }
    return JsonResult(status.HTTP_403_FORBIDDEN, meta, None, None)

