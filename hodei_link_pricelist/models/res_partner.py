# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def create(self, vals):
        res = super(ResPartner, self).create(vals)
        company_id = self.env.user.company_id.id
        o_company = self.env['res.company'].search([('id', '!=', company_id)])[0]
        res_id = 'res.partner,' + str(res.id)
        if vals.get('property_product_pricelist'):
            pricelist = self.env['product_pricelist'].search([('id', '=', vals['property_product_pricelist'])])
            self.env['ir.property'].write({
                'name': 'property_payment_term_id',
                'company_id': o_company['id'],
                'res_id': res_id,
                'fields_id': 2435,
                'value_reference': 'product.pricelist,' + pricelist['id'],
                'type': 'many2one'
            })
        return res
