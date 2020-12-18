# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.model
    def _default_route(self):
        return self.env['stock.location.route'].search([('default_route', '=', True), ('company_id', '=', self._context.get('order_id').get('company_id'))], limit=1)


    @api.onchange('company_id')
    def on_company_id(self):
        # Check if an other default_route is set for this company
        if self.company_id:
            self.route_id = self.env['stock.location.route'].search([('default_route', '=', True), ('company_id', '=', self.company_id)])

