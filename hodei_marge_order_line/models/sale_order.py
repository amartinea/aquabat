# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    marge_negative = fields.Boolean('Check marge', default=False)
    one_line_consu = fields.Boolean('Check consu line', default=False)

    @api.onchange('order_line')
    def on_change_order_line(self):
        marge_negative = False
        one_line_consu = False
        for line in self.order_line:
            if line.margin < 0 or marge_negative:
                marge_negative = True
            else:
                marge_negative = False

            if line.product_id.type == 'consu' or one_line_consu:
                one_line_consu = True
            else:
                one_line_consu = False
        self.marge_negative = marge_negative
        self.one_line_consu = one_line_consu

    def update_purchase_price_lines(self):
        for lines in self.order_line:
            if lines.product_id.cost_price != 0:
                lines.purchase_price = lines.product_id.cost_price
        self.on_change_order_line()
