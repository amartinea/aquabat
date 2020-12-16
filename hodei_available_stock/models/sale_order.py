# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    available_stock = fields.Selection([
        ('red', 'Red'),
        ('orange', 'Orange'),
        ('green', 'Green')], 
        'Available Stock', compute="_compute_available_stock")
    available_stock_company = fields.Float('Available Stock Company', compute="_compute_available_stock")
    available_stock_global = fields.Float('Available Stock Global', compute="_compute_available_stock")

    @api.onchange('product_uom_qty')
    def _compute_available_stock(self):
        for line in self:
        	if line.product_id:
                line.available_stock_global = line.product_id.qty_real_available
                line.available_stock_company = line.product_id._compute_quantities_dict_by_company(line.order_id.company_id.id)
                try:
                    if line.order_id.company_id:
                        if line.product_id._compute_quantities_dict_by_company(line.order_id.company_id.id) >= line.product_qty:
                            line.available_stock = 'green'
                        else:
                            line.available_stock = 'orange'
                
                        if line.product_id.qty_real_available < line.product_qty:
                            line.available_stock = 'red'
                except:
                    line.available_stock = False

    @api.onchange('product_id')
    def available_stock_change(self):
        if not self.product_id:
            self.available_stock_company = 0.0
            self.available_stock_global = 0.0
            return
        if self.product_id:
            self.available_stock_company = self.product_id.qty_real_available
            self.available_stock_global = self.product_id._compute_quantities_dict_by_company(self.order_id.company_id.id)
