export default {
  root: [{
    name: 'Sueldos',
    icon: 'fa fa-calculator',
    items: [{
      name: 'Sueldos 1',
      icon: 'fa fa-calculator',
      url: '/sueldos1/',
      permission: 'ejemplo_view'
    }, {
      name: 'Sueldos 2',
      icon: 'fa fa-calculator',
      url: '/sueldos1/',
      permission: 'ejemplo_view'
    }, {
      name: 'Sueldos 3',
      icon: 'fa fa-calculator',
      url: '/sueldos1/',
      permission: 'ejemplo_view'
    }, {
      name: 'Sueldos 4',
      icon: 'fa fa-calculator',
      url: '/sueldos1/',
      permission: 'ejemplo_view'
    }, {
      name: 'Sueldos 5',
      icon: 'fa fa-calculator',
      url: '/sueldos1/',
      permission: 'ejemplo_view'
    }, {
      name: 'Sueldos Multi',
      icon: 'fa fa-calculator',
      children: [{
          name: 'Sueldos Multi 1',
          url: '/sueldos6/sueldosmulti1/',
          permission: 'ejemplo_view'
        },
        {
          name: 'Sueldos Multi 2',
          url: '/sueldos6/sueldosmulti2/',
          permission: 'ejemplo_view'
        },
        {
          name: 'Sueldos Multi 3',
          url: '/sueldos6/sueldosmulti3/',
          permission: 'ejemplo_view'
        },
        {
          name: 'Sueldos Multi 4',
          url: '/sueldos6/sueldosmulti4/',
          permission: 'ejemplo_view'
        },
      ]
    }, ]
  }, {
    name: 'IVA',
    icon: 'fa fa-usd',
    items: [{
      name: 'IVA 1',
      icon: 'fa fa-usd',
      url: '/IVA/',
      permission: 'ejemplo_view'
    }, {
      name: 'IVA 2',
      icon: 'fa fa-usd',
      url: '/sueldos1/',
      permission: 'ejemplo_view'
    }, {
      name: 'IVA 3',
      icon: 'fa fa-usd',
      url: '/sueldos1/',
      permission: 'ejemplo_view'
    }, {
      name: 'IVA 4',
      icon: 'fa fa-usd',
      url: '/sueldos1/',
      permission: 'ejemplo_view'
    }, {
      name: 'IVA 5',
      icon: 'fa fa-usd',
      url: '/sueldos1/',
      permission: 'ejemplo_view'
    }, {
      name: 'IVA Multi',
      icon: 'fa fa-usd',
      children: [{
          name: 'IVA Multi 1',
          url: '/sueldos6/sueldosmulti1/',
          permission: 'ejemplo_view'
        },
        {
          name: 'IVA Multi 2',
          url: '/sueldos6/sueldosmulti2/',
          permission: 'ejemplo_view'
        },
        {
          name: 'IVA Multi 3',
          url: '/sueldos6/sueldosmulti3/',
          permission: 'ejemplo_view'
        },
        {
          name: 'IVA Multi 4',
          url: '/sueldos6/sueldosmulti4/',
          permission: 'ejemplo_view'
        },
      ]
    }, ]
  }, {
    name: 'Usuarios',
    icon: 'icon-user',
    items: [{
        name: 'Usuarios',
        url: '/usuarios/usuarios/',
        icon: 'fa fa-user',
        permission: 'usuarios_view'
      },
      {
        name: 'Permisos',
        url: '/usuarios/permisos/',
        icon: 'fa fa-lock',
        permission: 'superadmin'
      },
      {
        name: 'Grupos',
        url: '/usuarios/grupos/',
        icon: 'fa fa-users',
        permission: 'grupos_view'
      },
    ]
  }, {
    name: 'Configuracion',
    icon: 'fa fa-cog',
    items: [{
        name: 'Geográficas',
        icon: 'fa fa-map',
        children: [{
            name: 'Localidades',
            url: '/configuracion/geo/localidades/',
            permission: 'ejemplo_view'
          },
          {
            name: 'Provincias',
            url: '/configuracion/geo/provincias/',
            permission: 'ejemplo_view'
          },
          {
            name: 'Areas',
            url: '/configuracion/geo/areas/',
            permission: 'ejemplo_view'
          },
          {
            name: 'Nacionalidades',
            url: '/configuracion/geo/nacionalidades/',
            permission: 'ejemplo_view'
          },
        ]
      },
      {
        name: 'Contables',
        icon: 'fa fa-line-chart',
        children: [{
            name: 'Monedas',
            url: '/configuracion/contables/monedas/',
            permission: 'ejemplo_view'
          },
          {
            name: 'Puntos de Venta',
            url: '/configuracion/contables/puntosdeventa/',
            permission: 'ejemplo_view'
          },
          {
            name: 'Situacion de IVA',
            url: '/configuracion/contables/situacioniva/',
            permission: 'ejemplo_view'
          },
          {
            name: 'Tipos de Doc',
            url: '/configuracion/contables/tiposdedocumento/',
            permission: 'ejemplo_view'
          },
          {
            name: 'Tipos de Valor',
            url: '/configuracion/contables/tiposdevalor/',
            permission: 'ejemplo_view'
          },
        ]
      },

    ]
  }, ]
};