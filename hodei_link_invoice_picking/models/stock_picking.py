# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class StockPicking(models.Model):
    _inherit = "stock.picking"

    invoice_id = fields.Many2one('account.invoice', string='Invoice', default=False)
