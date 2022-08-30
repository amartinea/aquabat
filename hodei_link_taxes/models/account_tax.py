# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountTax(models.Model):
    _inherit = "account.tax"

    link_tax_id = fields.Many2one('account.tax', string='Tax for the other company', default=False)
