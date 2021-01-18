# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def _onchange_discount_product(self):
        _logger.info(self.product_id)
        _logger.info("product")
        _logger.info(self.product_uom_qty)
        _logger.info("qty")
        _logger.info(self.price_unit)
        _logger.info("price_unit")
        super(SaleOrderLine, self)._onchange_discount()

    @api.onchange('price_unit', 'product_uom', 'product_uom_qty', 'tax_id')
    def _onchange_discount(self):
        _logger.info(self.product_id)
        _logger.info("product")
        _logger.info(self.product_uom_qty)
        _logger.info("qty")
        _logger.info(self.price_unit)
        _logger.info("price_unit")
        super(SaleOrderLine, self)._onchange_discount()


    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        price_unit = self.price_unit
        super(SaleOrderLine, self).product_uom_change()
        self.price_unit = price_unit
