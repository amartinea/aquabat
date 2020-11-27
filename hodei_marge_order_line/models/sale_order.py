# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    marge_negative = fields.Boolean('Check marge', default=False)

    @api.onchange('order_line')
    def on_change_order_line(self):
        for line in self.order_line:
            _logger.info(line.margin)
            if line.margin < 0 or self.marge_negative:
                self.marge_negative = True
                return False
            else:
                self.marge_negative = False
    def update_purchase_price_lines(self):
        for lines in self.order_line:
            if lines.product_id.standard_price != 0:
                lines.purchase_price = lines.product_id.standard_price
