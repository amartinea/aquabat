# -*- coding: utf-8 -*-

from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model_create_multi
    def create(self, vals):
        if 'taxes_id' in vals and len(vals['taxes_id']) == 1:
            vals['taxes_id'] += self.env['account.tax'].search([('id', '!=', vals['taxes_id'])])['link_tax_id']['id']
        return super(ProductTemplate, self).create(vals)
