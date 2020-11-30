# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class AccountJournal(models.Model):
    _inherit = "account.journal"

    @api.multi
    def open_action(self):

        action = super(AccountJournal, self).open_action()
        action.update({'context': (action.get('context') or '') + "'search_default_company': 1"})
        return action
