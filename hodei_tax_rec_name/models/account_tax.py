# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class AccountTax(models.Model):
    _inherit = 'account.tax'
    _rec_name = 'description'
