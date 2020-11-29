# -*- coding: utf-8 -*-

{
    'name': 'Hodei Invoice Sending Preference module',
    'version': '1.0.0',
    'category': '',
    'description': """ """,
    'depends': [
        'account',
        'base',
        'sale',
    ],
    'external_dependencies': {
    },
    'data': [
        'views/account_invoice_view.xml',
        'views/res_partner_view.xml'
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
