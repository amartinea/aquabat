# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    marge_percent = fields.Float('Marge %', compute='_compute_marge', store=True)

    @api.depends('margin', 'amount_untaxed')
    def _compute_marge(self):
        for order in self:
            if order.amount_untaxed != 0:
                order.marge_percent = order.margin / order.amount_untaxed * 100
            else:
                order.marge_percent = 0
