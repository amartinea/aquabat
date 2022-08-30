# -*- coding: utf-8 -*-

from odoo import fields, models
import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = "res.partner"

    def create(self, vals):
        res = super(ResPartner, self).create(vals)
        company_id = self.env.user.company_id.id
        o_company = self.env['res.company'].search([('id', '!=', company_id)])[0]
        res_id = 'res.partner,' + str(res.id)
        if vals.get('property_payment_term_id'):
            term = self.env['account.payment.term'].search([('id', '=', vals['property_payment_term_id'])])
            self.env['ir.property'].sudo().create({
                'name': 'property_payment_term_id',
                'company_id': o_company['id'],
                'res_id': res_id,
                'fields_id': 2435,
                'value_reference': 'account.payment.term,' + str(term['link_payment_term_id']['id']),
                'type': 'many2one'
            })
        if vals.get('property_supplier_payment_term_id'):
            term = self.env['account.payment.term'].search([('id', '=', vals['property_supplier_payment_term_id'])])
            self.env['ir.property'].sudo().create({
                'name': 'property_supplier_payment_term_id',
                'company_id': o_company['id'],
                'res_id': res_id,
                'fields_id': 2422,
                'value_reference': 'account.payment.term,' + str(term['link_payment_term_id']['id']),
                'type': 'many2one'
            })
        return res
