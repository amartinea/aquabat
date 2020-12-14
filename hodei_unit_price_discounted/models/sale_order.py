# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    unit_price_net = fields.Float('Unit price net', compute="_compute_unit_price_net", store=True)

    @api.depends('price_unit', 'price_reduce_taxexcl')
    def _compute_unit_price_net(self):
        for line in self:
            line.unit_price_net = line.price_unit - line.price_reduce_taxexcl
