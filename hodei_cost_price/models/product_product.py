# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = "product.product"

    cost_price = fields.Float('Cost price', company_dependent=True)
    coef_item_ids = fields.Many2many('product.coeflist.item', 'Coeflist Items', compute='_get_coeflist_items')

    @api.one
    def _get_coeflist_items(self):
        self.coef_item_ids = self.env['product.coeflist.item'].search([
            '|', '|',
            ('product_id', '=', self.id),
            ('product_tmpl_id', '=', self.product_tmpl_id.id)]).ids

    def calcul_cost_price(self, standard_price):
        _logger.warning('calcul______________')
        for product in self:
            coeflist_items = self.env['product.coeflist.item'].search([
                '|', '|', ('categ_id', '=', product.categ_id.id),
                ('product_id', '=', product.id),
                ('product_tmpl_id', '=', product.product_tmpl_id.id)])
            coef_categ = 0
            coef_product = 0
            coef = 1
            for coeflist_item in coeflist_items:
                if coeflist_item.product_tmpl_id:
                    coef_product = coeflist_item.coef_value
                if coeflist_item.categ_id:
                    coef_categ = coeflist_item.coef_value
            if coef_categ != 0:
                coef = coef_categ
            if coef_product != 0:
                coef = coef_product
            _logger.warning('self.env.user.company_id.id______________')
            _logger.warning(self.env.user.company_id.id)
            product.cost_price = standard_price * coef
            if product.product_tmpl_id:   #Not exist when create product
                product.product_tmpl_id.cost_price = standard_price * coef

    @api.multi
    def write(self, values):
        _logger.warning('write________________________')
        res = super(ProductProduct, self).write(values)
        if 'standard_price' in values:
            self.calcul_cost_price(values['standard_price'])
        return res


class ProductTemplate(models.Model):
    _inherit = "product.template"

    cost_price = fields.Float('Cost price', compute='_compute_cost_price')

    @api.depends('product_variant_ids', 'product_variant_ids.standard_price')
    def _compute_cost_price(self):
        _logger.warning('oui______________')
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.cost_price = template.product_variant_ids.cost_price
        for template in (self - unique_variants):
            template.cost_price = 0.0

    @api.one
    def _set_cost_method(self):
        _logger.warning('_set_cost_method________________________')
        return super(ProductTemplate, self)._set_cost_method()
