# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    route_id = fields.Many2one(readonly=False)

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        result = super(SaleOrderLine, self).product_id_change()
        _logger.info(self.order_id.use_second_route)
        if not self.order_id.use_second_route:
            route = self.env['stock.location.route'].search([('default_route', '=', True), ('company_id', '=', self.company_id.id)])
        else:
            route = self.env['stock.location.route'].search([('default_update_route', '=', True), ('company_id', '=', line.order_id.company_id.id)])
        self.update({'route_id': route})
        return result

    # @api.multi
    # @api.depends('order_id.company_id')
    # def _on_change_company_id(self):
    #     for line in self:
    #         if line.order_id.company_id:
    #             line.route_id = self.env['stock.location.route'].search([('default_route', '=', True), ('company_id', '=', line.order_id.company_id.id)])

    # def write(self, vals):
    #     if self.order_id.company_id:
    #         vals['route_id'] = self.env['stock.location.route'].search([('default_route', '=', True), ('company_id', '=', self.order_id.company_id.id)])
    #     return super(SaleOrderLine, self).write(vals)
    # class SaleOrder(models.Model):
    #     _inherit = "sale.order"

class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    use_second_route = fields.Boolean(default=False)

    def use_alternative_route(self):
        for order in self:
            if order.company_id:
                order.use_second_route = True
                for line in order.order_line:
                    line.route_id = self.env['stock.location.route'].search([('default_update_route', '=', True), ('company_id', '=', line.order_id.company_id.id)])
