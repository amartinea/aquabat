# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"


    def write(self, vals):
    	payment_default = self.env['account.payment.term'].search([('default_term', '=', True)], limit=1)
    	if not vals['property_payment_term_id'] and payment_default:
    		vals['property_payment_term_id'] = payment_default
    	return super(ResPartner, self).write(vals)