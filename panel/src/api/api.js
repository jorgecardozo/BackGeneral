module.exports = {
    BASE_URL: BASE_URL,
    auth: BASE_URL + "auth/",
    clearToken: BASE_URL + "auth/clear-token/",
    authCheck: BASE_URL + "auth/check/",
    authCheckWithToken: BASE_URL + "auth/check-with-token/",
    authLogout: BASE_URL + "auth/logout/",
    authGetPermissions: BASE_URL + "auth/permissions/",
    dashboard: {
        stats: BASE_URL + "dashboard/",
    },
    usuarios: {
        perfil: BASE_URL + "usuarios/perfil/",
        usuarios: BASE_URL + "usuarios/usuarios/",
        permisos: BASE_URL + "usuarios/permisos/",
        grupos: BASE_URL + "usuarios/grupos/",
    },
    container: BASE_URL + "container/",
}