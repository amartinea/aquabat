# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"


    @api.multi
    def create_invoices(self):
        _logger.info('creates_invoices')
        super(SaleAdvancePaymentInv, self).create_invoices()
