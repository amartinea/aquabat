# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"


    route_id = fields.Many2one(compute='_compute_company_id')

    @api.multi
    @api.depends('order_id.company_id')
    def _compute_company_id(self):
        for line in self:
            if line.order_id.company_id:
                line.route_id = self.env['stock.location.route'].search([('default_route', '=', True), ('company_id', '=', line.order_id.company_id.id)])
