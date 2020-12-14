# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    available_stock = fields.Boolean('Available Stock', compute="_compute_available_stock")
    available_stock_company = fields.Float('Available Stock Global', compute="_compute_available_stock")
    available_stock_global = fields.Float('Available Stock Global', compute="_compute_available_stock")

    def _compute_available_stock(self):
        for line in self:
        	line.available_stock_global = line.product_id.qty_real_available
        	line.available_stock_company = line.product_id._compute_quantities_dict_by_company(line.order_id.company_id)
            try:
                if line.order_id.company_id:
                    if line.product_id._compute_quantities_dict_by_company(line.order_id.company_id) > line.product_qty:
                        line.available_stock = True
                    else:
                        line.available_stock = False
                
                        #if line.product_id.qty_real_available > line.product_qty:
                        #     line.available_stock = True
                        # else:
                        #     line.available_stock = False
            except:
                line.available_stock = False
