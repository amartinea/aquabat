# -*- coding: utf-8 -*-

{
    'name': 'Aquabat custom report module',
    'version': '1.0.0',
    'category': '',
    'description': """ """,
    'depends': [
        'account',
        'sale',
        'web',
    ],
    'external_dependencies': {
    },
    'data': [
        'report/report_delivery.xml',
        'report/report_delivery_without.xml',
        'report/report_invoice.xml',
        'report/report_sale.xml',
        'views/account_report.xml',
        'views/picking_report.xml',
        'views/sale_report.xml'
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
