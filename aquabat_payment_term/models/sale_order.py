# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    payment_term_id = fields.Many2one(
        'account.payment.term', string='Payment Terms', check_company=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", required=True)
