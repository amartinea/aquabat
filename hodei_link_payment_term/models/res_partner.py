# -*- coding: utf-8 -*-

from odoo import fields, models
import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = "res.partner"

    def write(self, values):
        res = super(ResPartner, self).write(values)
        company_id = self.env.user.company_id.id
        _logger('company_id :' + str(company_id))
        o_company = self.env['res.company'].search([('id', '!=', company_id)])[0]
        _logger('o_company :' + o_company)
        res_id = 'res.partner,' + str(self.id)
        _logger('res_id :' + res_id)
        _logger('values :' + values)
        if values.get('property_payment_term_id'):
            _logger('oui')
            term = self.env['account.payment.term'].search([('id', '=', values['property_payment_term_id'])])
            _logger('values :' + term)
            self.env['ir.property'].write({
                'name': 'property_payment_term_id',
                'company_id': o_company['id'],
                'res_id': res_id,
                'fields_id': 2435,
                'value_reference': 'account.payment.term' + term['link_payment_term_id']['id'],
                'type': 'many2one'
            })
        if values.get('property_supplier_payment_term_id'):
            _logger('oui')
            term = self.env['account.payment.term'].search([('id', '=', values['property_supplier_payment_term_id'])])
            self.env['ir.property'].write({
                'name': 'property_supplier_payment_term_id',
                'company_id': company_id,
                'res_id': res_id,
                'fields_id': 2422,
                'value_reference': 'account.payment.term' + term['link_payment_term_id']['id'],
                'type': 'many2one'
            })
        return res
