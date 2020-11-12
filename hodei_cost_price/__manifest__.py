# -*- coding: utf-8 -*-

{
    'name': 'Hodei custom cost price module',
    'version': '1.0.0',
    'category': '',
    'description': """ """,
    'depends': [
        'product',
        'sale',
        'sale_margin'
    ],
    'external_dependencies': {
    },
    'data': [
        'security/product_coeflist_security.xml',
        'security/ir.model.access.csv',
        'views/product_coeflist_views.xml',
        'views/product_product_views.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
