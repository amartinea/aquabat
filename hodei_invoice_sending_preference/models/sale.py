# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()

        sending_preference = 'none'
        if self.partner_invoice_id.sending_preference != 'none':
            sending_preference = self.partner_invoice_id.sending_preference
        elif self.partner_invoice_id.parent_id:
            sending_preference = self.partner_invoice_id.parent_id.sending_preference

        invoice_vals['sending_preference'] = sending_preference
        return invoice_vals
