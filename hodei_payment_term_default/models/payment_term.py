# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountPaymentTerm(models.Model):
    _inherit = "account.payment.term"

    default_term = fields.Boolean('Default term', default=False)

    @api.onchange('default_term')
    def on_default_term(self):
        # Check if an other default_term is set
        if 'default_term' in self and self['default_term']:
            already_set = self.env['account.payment.term'].search([('default_term', '=', True)])
            if already_set:
                raise UserError(_('An other payment term is set to be the default one : %s') % already_set.name)
            else:
                self.default_term = True

    def write(self, vals):
        if vals['default_term']:
            if 'default_term' in vals and vals['default_term'] == True:
                # Check if an other default_term is set
                already_set = self.env['account.payment.term'].search([('default_term', '=', True)])
                if already_set:
                    raise UserError(_('An other payment term is set to be the default one : %s') % already_set.name)
                    vals['default_term'] = False
        return super(AccountPaymentTerm, self).write(vals)
