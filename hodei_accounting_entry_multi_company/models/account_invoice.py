# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.model
    def finalize_invoice_move_lines(self, line):
    	console.log('---------------------ici----------------')
    	console.log(line)
        return line
