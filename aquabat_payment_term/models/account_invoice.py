# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountInvoice(models.Model):
	_inherit = "account.invoice"

	payment_term_id = fields.Many2one('account.payment.term', string='Payment Terms', oldname='payment_term',
		readonly=True, states={'draft': [('readonly', False)]},
		help="If you use payment terms, the due date will be computed automatically at the generation "
			"of accounting entries. If you keep the payment terms and the due date empty, it means direct payment. "
			"The payment terms may compute several due dates, for example 50% now, 50% in one month.", required=True)
