# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.model
    def _default_route(self):
        return self.env['stock.location.route'].search([('default_route', '=', True), ('company_id', '=', self.order_id.company_id)], limit=1)

    route_id = fields.many2one(default=_default_route)
