# -*- coding: utf-8 -*-

from odoo import fields, models
import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = "res.partner"

    def create(self, vals):
        res = super(ResPartner, self).create(vals)
        _logger.warning('res :')
        _logger.warning(res)
        _logger.warning('vals :')
        _logger.warning(vals)
        company_id = self.env.user.company_id.id
        o_company = self.env['res.company'].search([('id', '!=', company_id)])[0]
        res_id = 'res.partner,' + str(self.id)
        if vals.get('property_payment_term_id'):
            _logger.warning('oui')
            term = self.env['account.payment.term'].search([('id', '=', vals['property_payment_term_id'])])
            self.env['ir.property'].sudo().create({
                'name': 'property_payment_term_id, test',
                'company_id': o_company['id'],
                'res_id': res_id,
                'fields_id': 2435,
                'value_reference': 'account.payment.term' + str(term['link_payment_term_id']['id']),
                'type': 'many2one'
            })
        if vals.get('property_supplier_payment_term_id'):
            _logger.warning('oui')
            term = self.env['account.payment.term'].search([('id', '=', vals['property_supplier_payment_term_id'])])
            self.env['ir.property'].sudo().create({
                'name': 'property_supplier_payment_term_id, test',
                'company_id': company_id,
                'res_id': res_id,
                'fields_id': 2422,
                'value_reference': 'account.payment.term' + str(term['link_payment_term_id']['id']),
                'type': 'many2one'
            })
        return res
    def write(self, values):
        res = super(ResPartner, self).write(values)
        company_id = self.env.user.company_id.id
        _logger.warning('company_id :')
        _logger.warning(company_id)
        o_company = self.env['res.company'].search([('id', '!=', company_id)])[0]
        _logger.warning('o_company :')
        _logger.warning(o_company)
        res_id = 'res.partner,' + str(self.id)
        _logger.warning('res_id :')
        _logger.warning(res_id)
        _logger.warning('values :')
        _logger.warning(values)
        if values.get('property_payment_term_id'):
            _logger.warning('oui')
            term = self.env['account.payment.term'].search([('id', '=', values['property_payment_term_id'])])
            _logger.warning('values :')
            _logger.warning(term)
            self.env['ir.property'].write({
                'name': 'property_payment_term_id, test',
                'company_id': o_company['id'],
                'res_id': res_id,
                'fields_id': 2435,
                'value_reference': 'account.payment.term' + str(term['link_payment_term_id']['id']),
                'type': 'many2one'
            })
        if values.get('property_supplier_payment_term_id'):
            _logger.warning('oui')
            term = self.env['account.payment.term'].search([('id', '=', values['property_supplier_payment_term_id'])])
            self.env['ir.property'].write({
                'name': 'property_supplier_payment_term_id, test',
                'company_id': company_id,
                'res_id': res_id,
                'fields_id': 2422,
                'value_reference': 'account.payment.term' + str(term['link_payment_term_id']['id']),
                'type': 'many2one'
            })
        return res
