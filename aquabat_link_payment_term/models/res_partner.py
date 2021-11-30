# -*- coding: utf-8 -*-

from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model_create_multi
    def create(self, vals):
        new_partner = super(ResPartner, self).create(vals)
        _logger.warning(new_partner)
        if new_partner['property_payment_term_id']:
            property_to_copy = new_partner.property_payment_term_id.link_payment_term_id
            _logger.warning(property_to_copy)
            if new_partner.company_id.id == 1:
                _logger.warning('__________________________1')
                new_partner.with_context(force_company=3).write({'property_payment_term_id': property_to_copy.id})
            elif new_partner.company_id.id == 3:
                _logger.warning('__________________________3')
                new_partner.with_context(force_company=1).write({'property_payment_term_id': property_to_copy.id})
