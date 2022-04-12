# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
import logging

_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.model
    def _run_fifo(self, move, quantity=None):
        _logger.warning('fifo_______________')
        tmp_value = super(StockMove, self)._run_fifo(move, quantity)
        return tmp_value