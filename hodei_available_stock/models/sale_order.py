# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    available_stock = fields.Char('Available Stock', compute="_compute_available_stock", store=True)

    def _compute_available_stock(self):
        for line in self:
            try:
                if line.product_id.qty_real_available > line.product_qty:
                    line.available_stock = 'green'
                else:
                    line.available_stock = 'red'
            except:
                line.available_stock = 'red'
