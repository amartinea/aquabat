# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _default_payment_term(self):
        return self.env['account.payment.term'].search([('default_term', '=', True)], limit=1)

    property_payment_term_id = fields.Many2one('account.payment.term', company_dependent=True,
        string='Customer Payment Terms',
        help="This payment term will be used instead of the default one for sales orders and customer invoices", 
        oldname="property_payment_term", default=_default_payment_term)
