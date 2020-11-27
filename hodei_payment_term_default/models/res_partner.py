# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def create(self, vals):
        payment_default = self.env['account.payment.term'].search([('default_term', '=', True)], limit=1)
        if vals['property_payment_term_id'] == False and payment_default:
            vals['property_payment_term_id'] = payment_default
        return super(ResPartner, self).create(vals)
