# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AccountInvoice(models.Model):
    _name = "account.invoice"

    fee_price = fields.Float('Value 2', compute="_compute_fee",)
    apply_fee = fields.Boolean(string='Apply Fee', default=True)

    @api.onchange('apply_fee', 'partner_id')
    def _compute_fee(self)
        if self.apply_fee:
            fee_line = self.partner_id.fee_id._check_condition_to_apply(self.amount_total)

            if fee_line.value_type == 'perc':
                fee_price = self.amount_total * fee_line.value_apply / 100
            elif fee_line.value_type == 'fix':
                fee_price = fee_line.value_apply
        else:
        	fee_price = 0
       	self.fee_price = fee_price
        self.update_invoice_values(fee_price, self.partner_id.fee_id.tax_id)

    def update_invoice_values(self, fee_price, tax_id):
        amount_untaxed += amount_untaxed + fee_price
        amount_tax += amount_tax + (fee_price * tax_id.amount / 100) 
        amount_total += amount_total + fee_price
