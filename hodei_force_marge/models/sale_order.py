# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    force_marge = fields.Boolean('Force marge', default=False)

    @api.model
    def create(self, vals):
        if vals['marge_negative'] == True:
            if vals['force_marge'] != True:
                raise ValidationError("Some line have negative marge. Fix it or check the force marge button")
        return super(SaleOrder, self).create(vals)
