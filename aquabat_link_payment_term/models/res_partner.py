# -*- coding: utf-8 -*-

from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.depends('property_payment_term_id')
    def _onchange_property_payment_term_id(self):
        property_to_copy = self.property_payment_term_id.link_payment_term_id
        _logger.warning(property_to_copy)
        if self.company_id.id == 1:
            _logger.warning('__________________________1')
            self.with_context(force_company=3).write({'property_payment_term_id': property_to_copy})
        elif self.company_id.id == 3:
            _logger.warning('__________________________3')
            self.with_context(force_company=1).write({'property_payment_term_id': property_to_copy})
