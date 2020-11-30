# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class AccountJournal(models.Model):
    _inherit = "account.journal"

    @api.multi
    def open_action(self):

        action = super(AccountJournal, self).open_action()
        action.update({'context': (action.get('context') or '').update({'search_default_company': 1})})
        _logger.warning("--------------------------------------")
        _logger.warning(action)
        return action
