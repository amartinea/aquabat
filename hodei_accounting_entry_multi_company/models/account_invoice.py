# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _inherit = "account.invoice"


    @api.model
    def finalize_invoice_move_lines(self, line):
        _logger.warning('--------------------ici-------------')
        _logger.warning(line)
        return line
