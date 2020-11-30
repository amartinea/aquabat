# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)

class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    sending_preference = fields.Selection([('none', ' '),('mail', 'Mail'),('postal', 'Postal')], 
    	string='Invoice Sending Preference', default='none')


    @api.onchange('partner_id')
    def _on_change_partner_id(self):
        if self.partner_id.sending_preference != 'none':
            self.sending_preference = self.partner_id.sending_preference
        elif self.partner_id.parent_id:
            self.sending_preference = self.partner_id.parent_id.sending_preference
        else:
            self.sending_preference = 'none'


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    @api.multi
    def _create_invoice(self, order, so_line, amount):
        invoice = super(SaleAdvancePaymentInv, self)._create_invoice(order, so_line, amount)
        _logger.warning("----- saleadvance -----")
        _logger.warning(invoice)
        _logger.warning(order)
        if order:
            if order.partner_id.sending_preference != 'none':
                sending_preference = order.partner_id.sending_preference
            elif order.partner_id.parent_id:
                sending_preference = order.partner_id.parent_id.sending_preference
            else:
                sending_preference = 'none'
            _logger.warning(sending_preference)
            invoice.write({'sending_preference': sending_preference})
            invoice.write({'customer_name': order['customer_name']})
        return invoice
