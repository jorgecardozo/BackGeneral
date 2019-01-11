from django.conf.urls import url,include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views as authviews

from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^', include('users.urls')),
    url(r'^', include('main.urls')),
    url(r'^', include('config.urls')),
    #url(r'^', include('Ejemplo.urls')),
    url(r'^', include('Personas.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
