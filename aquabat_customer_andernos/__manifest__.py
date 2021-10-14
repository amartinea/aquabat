# -*- coding: utf-8 -*-

{
    'name': 'Aquabat custom customer module',
    'version': '1.0.0',
    'category': '',
    'description': """ """,
    'depends': [
        'account',
        'aquabat_report_andernos',
        'delivery',
        'sale',
        'stock',
        'web',
    ],
    'external_dependencies': {
    },
    'data': [
        'report/report_sale.xml',
        'report/report_picking.xml',
        'report/report_invoice.xml',
        'views/account_invoice_views.xml',
        'views/sale_order_views.xml',
        'views/stock_picking_views.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
