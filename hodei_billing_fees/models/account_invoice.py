# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.tools import float_is_zero


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    fee_price = fields.Float('Billing Fee', compute="_compute_fee", store=True, default="0")
    apply_fee = fields.Boolean(string='Apply Fee', default=True)

    @api.depends('apply_fee', 'partner_id', 'invoice_line_ids')
    def _compute_fee(self):
        for invoice in self:
            if invoice.apply_fee:
                fee_line = invoice.partner_id.fee_id._check_condition_to_apply(invoice.amount_untaxed)
                if fee_line:
                    if fee_line.value_type == 'perc':
                        fee_price = invoice.amount_untaxed * fee_line.value_apply / 100
                    elif fee_line.value_type == 'fix':
                        fee_price = fee_line.value_apply
                else:
                    fee_price = 0
            else:
                fee_price = 0
            invoice.fee_price = fee_price


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

    @api.one
    @api.depends(
        'state', 'currency_id', 'invoice_line_ids.price_subtotal',
        'move_id.line_ids.amount_residual',
        'move_id.line_ids.currency_id')
    def _compute_residual(self):
        residual = 0.0
        residual_company_signed = 0.0
        sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
        for line in self._get_aml_for_amount_residual():
            residual_company_signed += line.amount_residual
            if line.currency_id == self.currency_id:
                residual += line.amount_residual_currency if line.currency_id else line.amount_residual
            else:
                if line.currency_id:
                    residual += line.currency_id._convert(line.amount_residual_currency, self.currency_id, line.company_id, line.date or fields.Date.today())
                else:
                    residual += line.company_id.currency_id._convert(line.amount_residual, self.currency_id, line.company_id, line.date or fields.Date.today())
        self.residual_company_signed = abs(residual_company_signed + (self.fee_price * self.partner_id.fee_id.tax_id.amount / 100)) * sign
        self.residual_signed = abs(residual + (self.fee_price * self.partner_id.fee_id.tax_id.amount / 100)) * sign
        self.residual = abs(residual + (self.fee_price * self.partner_id.fee_id.tax_id.amount / 100))
        digits_rounding_precision = self.currency_id.rounding
        if float_is_zero(self.residual, precision_rounding=digits_rounding_precision):
            self.reconciled = True
        else:
            self.reconciled = False
