# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class AccountTax(models.Model):
    _inherit = 'account.tax'


    @api.multi
    def name_get(self):
        result = []
        for record in self:
            record_name = record.description
            result.append((record.id, record_name))
        return result
