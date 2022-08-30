# -*- coding: utf-8 -*-

from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'taxes_id' in vals and len(vals['taxes_id'][0][2]) == 1:
                vals['taxes_id'][0][2].append(
                    self.env['account.tax'].search([('id', 'in', vals['taxes_id'][0][2])])['link_tax_id']['id'])
            if 'supplier_taxes_id' in vals and len(vals['supplier_taxes_id'][0][2]) == 1:
                vals['supplier_taxes_id'][0][2].append(
                    self.env['account.tax'].search([('id', 'in', vals['supplier_taxes_id'][0][2])])['link_tax_id'][
                        'id'])
        return super(ProductTemplate, self).create(vals_list)
