# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def create(self, vals):
        payment_default = self.env['account.payment.term'].search([('default_term', '=', True)], limit=1)
        _logger.warning("-----------------------")
        _logger.warning(vals)
        if vals['property_payment_term_id'] == False and payment_default:
            vals['property_payment_term_id'] = payment_default
        return super(ResPartner, self).create(vals)
