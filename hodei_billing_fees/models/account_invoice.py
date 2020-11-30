# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)

class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    fee_price = fields.Float('Billing Fee', compute="_compute_fee", store=True)
    apply_fee = fields.Boolean(string='Apply Fee', default=True)

    @api.depends('apply_fee', 'partner_id', 'invoice_line_ids')
    def _compute_fee(self):
        _logger.warning("----- Invoice -----")
        _logger.warning(self)
        if self.apply_fee:
            fee_line = self.partner_id.fee_id._check_condition_to_apply(self.amount_untaxed)
            if fee_line:
                if fee_line.value_type == 'perc':
                    fee_price = self.amount_untaxed * fee_line.value_apply / 100
                elif fee_line.value_type == 'fix':
                    fee_price = fee_line.value_apply
            else:
                fee_price = 0
        else:
            fee_price = 0
        _logger.warning("----- Fee -----")
        _logger.warning(fee_price)
        self.fee_price = fee_price


    @api.one
    @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'tax_line_ids.amount_rounding',
                 'currency_id', 'company_id', 'date_invoice', 'type', 'fee_price')
    def _compute_amount(self):
        round_curr = self.currency_id.round
        self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line_ids) + self.fee_price
        self.amount_tax = sum(round_curr(line.amount_total) for line in self.tax_line_ids) + (self.fee_price * self.partner_id.fee_id.tax_id.amount / 100) 
        self.amount_total = self.amount_untaxed + self.amount_tax
        amount_total_company_signed = self.amount_total
        amount_untaxed_signed = self.amount_untaxed
        if self.currency_id and self.company_id and self.currency_id != self.company_id.currency_id:
            currency_id = self.currency_id
            amount_total_company_signed = currency_id._convert(self.amount_total, self.company_id.currency_id, self.company_id, self.date_invoice or fields.Date.today())
            amount_untaxed_signed = currency_id._convert(self.amount_untaxed, self.company_id.currency_id, self.company_id, self.date_invoice or fields.Date.today())
        sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
        self.amount_total_company_signed = amount_total_company_signed * sign
        self.amount_total_signed = self.amount_total * sign
        self.amount_untaxed_signed = amount_untaxed_signed * sign
