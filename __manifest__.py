{
    'name': 'Rest API',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/rest_api_views.xml',
        'views/rest_api_menus.xml',
    ],
    'installable': True,
    'application': True

}
