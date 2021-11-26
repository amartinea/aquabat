# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountPaymentTerm(models.Model):
    _inherit = "account.payment.term"

    link_payment_term_id = fields.Many2one('account.payment.term', string='Payment link for the other company', domain=[('company_id', '!=', company_id)], default=False)
