# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    marge = fields.Float('Marge', compute='_compute_marge', store=True)
    marge_percent = fields.Float('Marge %', compute='_compute_marge', store=True)
    product_type = fields.Char('Product type', compute='_compute_type', store=True)

    @api.depends('product_uom_qty', 'purchase_price', 'price_subtotal')
    def _compute_marge(self):
        for line in self:
            if line.purchase_price:
                line.marge = line.price_subtotal - line.product_uom_qty * line.purchase_price
                if line.price_subtotal != 0:
                    line.marge_percent = (line.price_subtotal - line.product_uom_qty * line.purchase_price) * 100 / line.price_subtotal
                else:
                    line.marge_percent = 0

    @api.depends('product_id')
    def _compute_type(self):
        for line in self:
            if line.product_id.type:
                line.product_type = line.product_id.type
