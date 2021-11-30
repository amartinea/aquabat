# -*- coding: utf-8 -*-

from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    def write(self, vals):
        if 'property_payment_term_id' in vals and vals['property_payment_term_id']:
            property_to_copy = self.property_payment_term_id.link_payment_term_id
            _logger.warning(property_to_copy)
            _logger.warning(self.company_id)
            _logger.info(vals.company_id)
            if self.company_id.id == 1:
                _logger.warning('__________________________1')
                self.with_context(force_company=3).write({'property_payment_term_id': property_to_copy})
            elif self.company_id.id == 3:
                _logger.warning('__________________________3')
                self.with_context(force_company=1).write({'property_payment_term_id': property_to_copy})
