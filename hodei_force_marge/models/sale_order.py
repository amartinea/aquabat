# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    force_marge = fields.Boolean('Force marge', default=False)

    @api.model
    def create(self, vals):
        if vals['marge_negative'] == True:
            if vals['force_marge'] == True:
                return super(SaleOrder, self).create(vals)
            else:
                raise ValidationError("Some line have negative marge. Fix it or check the force marge button")
