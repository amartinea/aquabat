# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import logging

logger = logging.getLogger(__name__)

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    @api.multi
    def _compute_tax_id(self):
        for line in self:
            fpos = line.order_id.fiscal_position_id or line.order_id.partner_id.property_account_position_id
            # If company_id is set, always filter taxes by the company
            taxes = line.product_id.supplier_taxes_id.filtered(
                lambda r: not line.company_id or r.company_id == line.company_id)
            logger.warning('taxes:')
            logger.warning(taxes)
            line.taxes_id = fpos.map_tax(taxes, line.product_id, line.order_id.partner_id) if fpos else taxes
