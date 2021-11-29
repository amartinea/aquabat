# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.onchange('property_payment_term_id')
    def _onchange_property_payment_term_id(self):
        property_to_copy = self.property_payment_term_id.link_payment_term_id
        if self.company_id == 1:
            self.with_context(force_company=3).write({'property_payment_term_id': property_to_copy})
        elif self.company_id == 3:
            self.with_context(force_company=1).write({'property_payment_term_id': property_to_copy})
