# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    marge_negative = fields.Boolean('Check marge', default=False)

    @api.onchange('order_line')
    def on_change_order_line(self):
        marge_negative = False
        for line in self.order_line:
            if line.margin < 0 or marge_negative:
                marge_negative = True
            else:
                marge_negative = False
        self.marge_negative = marge_negative
    def update_purchase_price_lines(self):
        for lines in self.order_line:
            if lines.product_id.standard_price != 0:
                lines.purchase_price = lines.product_id.standard_price
        self.on_change_order_line()
