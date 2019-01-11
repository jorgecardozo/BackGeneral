from .constants import MessageErrorCodes
from rest_framework.exceptions import ErrorDetail


def ParseValidationErrors(errors):
    parsed_errors = ParseValidationDict(errors[0])
    return parsed_errors
    
def ParseValidationDict(dict_errors, prefix = ""):
    parsed_errors = dict()
    #print(dict_errors)
    for field in dict_errors.keys():
        fieldName = str(field)
        fieldErrors = dict_errors[field]
        _fieldErrors = None
        for fieldError in fieldErrors:
            if type(fieldError) == dict:
                if _fieldErrors == None:
                    _fieldErrors = []
                _fieldErrors.append(ParseValidationDict(fieldError))
                pass
            elif type(fieldError) == list:
                if _fieldErrors == None:
                    _fieldErrors = []
                pass
            elif type(fieldError) == str:
                if _fieldErrors == None:
                    _fieldErrors = {}
                for __error in fieldErrors[fieldError]:
                    _fieldErrors[fieldError] = [NewError("invalid", str(__error))]
                #_fieldErrors.append({fieldError: [NewError("invalid", str(__error)) for __error in fieldErrors[fieldError]]})
            else:
                if _fieldErrors == None:
                    _fieldErrors = []
                _fieldErrors.append(NewError(fieldError.code, str(fieldError)))
        parsed_errors[fieldName] = _fieldErrors
    return parsed_errors

def NewError(code, detail):
    return {
        'code': code,
        'detail': detail
    }