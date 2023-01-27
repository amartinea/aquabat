# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp


class ProductCoeflist(models.Model):
    _name = "product.coeflist"
    _description = "Coeflist"
    _order = "sequence asc, id desc"

    # def _get_default_item_ids(self):
    #     ProductCoeflistItem = self.env['product.coeflist.item']
    #     vals = ProductCoeflistItem.default_get(list(ProductCoeflistItem._fields))
    #     vals.update()
    #     return [[0, False, vals]]

    name = fields.Char('Coeflist Name', required=True, translate=True)
    active = fields.Boolean('Active', default=True, help="If unchecked, it will allow you to hide the coeflist without removing it.")
    item_ids = fields.One2many(
        'product.coeflist.item', 'coeflist_id', 'Coeflist Items',
        copy=True)
    company_id = fields.Many2one('res.company', 'Company')

    sequence = fields.Integer(default=16)
    country_group_ids = fields.Many2many('res.country.group', 'res_country_group_coeflist_rel',
                                         'coeflist_id', 'res_country_group_id', string='Country Groups')

class ResCountryGroup(models.Model):
    _inherit = 'res.country.group'

    coeflist_ids = fields.Many2many('product.coeflist', 'res_country_group_coeflist_rel',
                                     'res_country_group_id', 'coeflist_id', string='Coeflists')

class ProductCoeflistItem(models.Model):
    _name = "product.coeflist.item"
    _description = "Coeflist item"
    _order = "applied_on, categ_id desc, id"

    product_tmpl_id = fields.Many2one(
        'product.template', 'Product Template', ondelete='cascade',
        help="Specify a template if this rule only applies to one product template. Keep empty otherwise.")
    product_id = fields.Many2one(
        'product.product', 'Product', ondelete='cascade',
        help="Specify a product if this rule only applies to one product. Keep empty otherwise.")
    categ_id = fields.Many2one(
        'product.category', 'Product Category', ondelete='cascade',
        help="Specify a product category if this rule only applies to products belonging to this category or its children categories. Keep empty otherwise.")
    applied_on = fields.Selection([
        ('3_global', 'Global'),
        ('2_product_category', ' Product Category'),
        ('1_product', 'Product'),
        ('0_product_variant', 'Product Variant')], "Apply On",
        default='3_global', required=True,
        help='Coeflist Item applicable on selected option')

    base_coeflist_id = fields.Many2one('product.coeflist', 'Other Coeflist')
    coeflist_id = fields.Many2one('product.coeflist', 'Coeflist', index=True, ondelete='cascade')

    company_id = fields.Many2one(
        'res.company', 'Company',
        readonly=True, related='coeflist_id.company_id', store=True)
    date_start = fields.Date('Start Date', help="Starting date for the coeflist item validation")
    date_end = fields.Date('End Date', help="Ending valid for the coeflist item validation")
    coef_value = fields.Float('Coef Value')
    name = fields.Char(
        'Name', compute='_get_coeflist_item_name_coef',
        help="Explicit rule name for this coeflist line.")
    coef = fields.Char(
        'Coef', compute='_get_coeflist_item_name_coef',
        help="Explicit rule name for this coeflist line.")

    @api.constrains('coeflist_id')
    def _check_recursion(self):
        if any(item.coeflist_id and item.coeflist_id == item.base_coeflist_id for item in self):
            raise ValidationError(_('Error! You cannot assign the Main Coeflist as Other Coeflist in Coeflist Item!'))
        return True

    @api.one
    @api.depends('categ_id', 'product_tmpl_id', 'product_id', 'coef_value')
    def _get_coeflist_item_name_coef(self):
        if self.categ_id:
            self.name = _("Category: %s") % (self.categ_id.name)
        elif self.product_tmpl_id:
            self.name = self.product_tmpl_id.name
        elif self.product_id:
            self.name = self.product_id.display_name.replace('[%s]' % self.product_id.code, '')
        else:
            self.name = _("All Products")
        self.coef = _("%s coef") % (self.coef_value)

    @api.onchange('applied_on')
    def _onchange_applied_on(self):
        if self.applied_on != '0_product_variant':
            self.product_id = False
        if self.applied_on != '1_product':
            self.product_tmpl_id = False
        if self.applied_on != '2_product_category':
            self.categ_id = False

    def write(self, vals):
        product_coef_list = super(ProductCoeflistItem, self).write(vals)
        if 'product_tmpl_id' in self and self['product_tmpl_id']:
            products = self.env['product.product'].search([('product_tmpl_id', '=', self.product_tmpl_id.id)])
        if 'categ_id' in self and self['categ_id']:
            products = self.env['product.product'].search([('categ_id', '=', self.categ_id.id)])
        if 'applied_on' in self and self.applied_on == '3_global':
            products = self.env['product.product'].search([])
        for product in products:
            product.product_tmpl_id._compute_cost_price()
        return product_coef_list

    def unlink(self):
        products = self.env['product.product'].search([])
        for product in products:
            product.product_tmpl_id._compute_cost_price()
        return super(ProductCoeflistItem, self).unlink()

    def create(self, vals):
        product_coef_list = super(ProductCoeflistItem, self).create(vals)
        if 'product_tmpl_id' in vals[0] and vals[0]['product_tmpl_id']:
            products = self.env['product.product'].search([('product_tmpl_id', '=', vals[0]['product_tmpl_id'])])
        if 'categ_id' in vals[0] and vals[0]['categ_id']:
            products = self.env['product.product'].search([('categ_id', '=', vals[0]['categ_id'])])
        if 'applied_on' in vals[0] and vals[0]['applied_on'] == '3_global':
            products = self.env['product.product'].search([])
        for product in products:
            product.product_tmpl_id._compute_cost_price()
        return product_coef_list