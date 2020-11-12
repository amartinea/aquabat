# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    marge_negative = fields.Boolean('Check marge', default=False)

    @api.onchange('order_line')
    def on_change_order_line(self):
        for line in self.order_line:
            if line.margin < 0:
                self.marge_negative = True
                return False
            else:
                self.marge_negative = False
