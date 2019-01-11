from django.conf.urls import url,include
from django.views.decorators.csrf import csrf_exempt

from .resources import resources_auth, resources_grupos, resources_permisos, resources_usuarios

urlpatterns = [
    url(r'^auth/logout/', csrf_exempt(resources_auth.logout)),
    url(r'^auth/permissions/', resources_auth.get_permissions),
    url(r'^auth/check-with-token/', resources_auth.auth_check_with_token),
    url(r'^auth/clear-token/', resources_auth.clear_token),
    url(r'^auth/check/', csrf_exempt(resources_auth.auth_check)),
    url(r'^auth/', csrf_exempt(resources_auth.login)),
    
    url(r'^usuarios/perfil/$', resources_usuarios.perfil),

    url(r'^usuarios/usuarios/$', resources_usuarios.list),
    url(r'^usuarios/usuarios/(?P<id>[0-9]+)/$', resources_usuarios.detail),
    
    url(r'^usuarios/usuarios/export/$', resources_usuarios.getExportToken),
    url(r'^usuarios/usuarios/export/(?P<token>.*)$', resources_usuarios.export),

    url(r'^usuarios/permisos/$', resources_permisos.list),
    url(r'^usuarios/permisos/(?P<id>[0-9]+)/$', resources_permisos.detail),

    url(r'^usuarios/permisos/export/$', resources_permisos.getExportToken),
    url(r'^usuarios/permisos/export/(?P<token>.*)$', resources_permisos.export),

    url(r'^usuarios/grupos/$', resources_grupos.list),
    url(r'^usuarios/grupos/(?P<id>[0-9]+)/$', resources_grupos.detail),

    url(r'^usuarios/grupos/export/$', resources_grupos.getExportToken),
    url(r'^usuarios/grupos/export/(?P<token>.*)$', resources_grupos.export),

]