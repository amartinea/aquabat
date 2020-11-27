# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


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
