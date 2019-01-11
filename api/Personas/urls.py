from django.conf.urls import url,include
from .resources import resources

urlpatterns = [
    url(r'^personas/$', resources.list),
    url(r'^personas/(?P<id>[0-9]+)/$', resources.detail),
]