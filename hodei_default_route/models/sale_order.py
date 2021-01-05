# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _default_route(self):
        _logger.info("default_route")
        if self.order_id.company_id:
            _logger.info("company_id")
            return self.env['stock.location.route'].search([('default_route', '=', True), ('company_id', '=', self.order_id.company_id.id)])

    route_id = fields.Many2one(default=lambda self: self._default_route(), readonly=False)

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

    #     def _use_alternative_route(self):
    #         for order in self:
    #             if order.company_id:
    #                 for line in order.order_line: 
    #                     line.route_id = self.env['stock.location.route'].search([('default_update_route', '=', True), ('company_id', '=', line.order_id.company_id.id)])
