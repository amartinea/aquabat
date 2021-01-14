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
        'report/external_layout.xml',
        'report/external_layout_hf.xml',
        'report/report_delivery.xml',
        'report/report_delivery_without_payment.xml',
        'report/report_invoice.xml',
        'report/report_invoice_without_payment.xml',
        'report/sale_order_report.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
