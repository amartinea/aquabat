# -*- coding: utf-8 -*-

from odoo import fields, models


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    link_product_pricelist_id = fields.Many2one('product.pricelist', string='Product Pricelist for the other company', default=False)
