# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_id_check = fields.Char(string='Product Check')

    @api.onchange('product_id', 'price_unit', 'product_uom', 'product_uom_qty', 'tax_id')
    def _onchange_discount(self):
        """
        This function will not be easy to bring to next Odoo version

        Here to fix the discount value after a user modification
        Update it only when the product_id changed

        The way to do that is dirty :
         - Use a product_id_check as flag
         - The flag is set to True after the first time within onchange
         - The flag is reset at every new user action (dirty/strange)
         - As long as the flag is False, the discount value is kept
         - Discount is update when the flag is True

        This system work because this method is triggered many time only when the product value is updated
        """
        if self.product_id_check != 'check':
            discount = self.discount

        super(SaleOrderLine, self)._onchange_discount()

        if self.product_id_check != 'check':
            self.discount = discount
        self.product_id_check = 'check'



    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        price_unit = self.price_unit
        super(SaleOrderLine, self).product_uom_change()
        self.price_unit = price_unit
