# -*- coding: utf-8 -*-

from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model_create_multi
    def create(self, vals_list):
        _logger.warning(vals_list)
        for vals in vals_list:
            _logger.warning(vals['taxes_id'])
            _logger.warning(vals['taxes_id'][0])
            if 'taxes_id' in vals and len(vals['taxes_id'][0][2]) == 1:
                vals['taxes_id'][0][2] += self.env['account.tax'].search([('id', '=', vals['taxes_id'][0][2])])['link_tax_id']['id']
            _logger.warning(vals)
        return super(ProductTemplate, self).create(vals_list)
