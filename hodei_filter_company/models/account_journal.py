# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class AccountJournal(models.Model):
    _inherit = "account.journal"

    @api.multi
    def open_action(self):

        action = super(AccountJournal, self).open_action()
        context = action.get('context') or {}
        context['search_default_company'] = 1
        action.update({'context': context})
        return action
