# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_id_check = fields.Char(string='Product Check')

    @api.onchange('product_id', 'price_unit', 'product_uom', 'product_uom_qty', 'tax_id')
    def _onchange_discount(self):
        if self.discount != 0 and self.product_id_check and self.product_id_check == 'check':
            _logger.info("oui")
            _logger.info(self.discount)
            discount = self.discount
            super(SaleOrderLine, self)._onchange_discount()
            self.discount = discount
            self.product_id_check = 'check'
        else:
            _logger.info("non")
            _logger.info(self.discount)
            _logger.info(self.product_id_check)
            _logger.info(self.product_id)
            if self.product_id_check != 'check':
                discount = self.discount
            super(SaleOrderLine, self)._onchange_discount()
            if self.product_id_check != 'check':
                self.discount = discount
            self.product_id_check = 'check':
            _logger.info(self.discount)


    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        price_unit = self.price_unit
        super(SaleOrderLine, self).product_uom_change()
        self.price_unit = price_unit
