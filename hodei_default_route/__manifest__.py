# -*- coding: utf-8 -*-

{
    'name': 'Hodei Default Route module',
    'version': '1.0.0',
    'category': '',
    'description': """ """,
    'depends': [
        'sale',
        'stock',
    ],
    'external_dependencies': {
    },
    'data': [
        'views/account_invoice_view.xml',
        'views/purchase_order_view.xml',
        'views/sale_order_view.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
