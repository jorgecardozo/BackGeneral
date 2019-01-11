from ..models import Grupos

def Exists(id):
    """
    Devuelve True o Falso de acuerdo a si existe o no.
    """
    return Grupos.objects.filter(id=id).exists()
