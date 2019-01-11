from ..models import Personas

def Exists(id):
    """
    Devuelve True o Falso de acuerdo a si existe o no.
    """
    return Personas.objects.filter(id=id).exists()