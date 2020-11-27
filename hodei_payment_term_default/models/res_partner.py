# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class ResPartner(models.Model):
    _inherit = "res.partner"


    property_payment_term_id = fields.Many2one('account.payment.term', company_dependent=True,
        string='Customer Payment Terms',
        help="This payment term will be used instead of the default one for sales orders and customer invoices", 
        oldname="property_payment_term", default=lambda self: self.env['account.payment.term'].search([('default_term', '=', True)])[0])
