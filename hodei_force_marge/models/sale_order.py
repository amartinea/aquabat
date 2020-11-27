# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    force_marge = fields.Boolean('Force marge', default=False)

    def create(self):
        if self['marge_negative'] == True:
            if self['force_marge'] == True:
                return super(SaleOrder, self).create()
            else:
                raise ValidationError("Some line have negative marge. Fix it or check the force marge button")
