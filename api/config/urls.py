from django.conf.urls import url,include
from django.views.decorators.csrf import csrf_exempt

from . import resources

urlpatterns = [
    url(r'^config/default/$', resources.detail),
]