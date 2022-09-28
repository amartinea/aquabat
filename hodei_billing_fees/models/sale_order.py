# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    fee_price = fields.Float('Billing Fee', store=True, default="0")
    apply_fee = fields.Boolean(string='Apply Fee', default=True)

    @api.model
    def create(self, vals):
        _logger.warning(self)
        _logger.warning(vals)
        _logger.warning(vals)
        amount_change = 0
        if vals.get('order_line'):
            for line in vals['order_line']:
                if line[0] == 0:
                    _logger.warning('tax_id')
                    _logger.warning(line[2]['price_unit'])
                    _logger.warning(line[2]['discount'])
                    _logger.warning(1 - (line[2]['discount'] or 0.0) / 100)
                    amount_change += line[2]['product_uom_qty'] * (
                                line[2]['price_unit'] * (1 - (line[2]['discount'] or 0.0) / 100))
                elif line[0] == 2:
                    amount_change -= self.env['sale.order.line'].search([('id', '=', line[1])])['price_subtotal']
                _logger.warning('amount_change row')
                _logger.warning(amount_change)
        if vals['apply_fee']:
            partner = self.env['res.partner'].search([('id', '=', vals['partner_id'])])
            _logger.warning('amount_change')
            _logger.warning(amount_change)
            if self.company_id.id == partner.fee_id.company_id.id:
                fee_line = partner.fee_id._check_condition_to_apply(amount_change)
            else:
                fee_line = partner.fee_id.fee_linked._check_condition_to_apply(amount_change)
            _logger.warning(fee_line)
            if fee_line:
                if fee_line.value_type == 'perc':
                    fee_price = vals['amount_untaxed'] * fee_line.value_apply / 100
                elif fee_line.value_type == 'fix':
                    fee_price = fee_line.value_apply
            else:
                fee_price = 0
        else:
            fee_price = 0
        if fee_price != 0:
            flag_fee = 0
            for line in vals['order_line']:
                if line[2]['product_id'] == self.env.ref('hodei_billing_fees.product_fees').id:
                    flag_fee = 1
            if flag_fee == 0:
                sale_line_data = {
                    'name': 'Billing Fee',
                    'product_id': self.env.ref('hodei_billing_fees.product_fees').id,
                    'price_unit': fee_price,
                    'price_subtotal': fee_price,
                    'price_total': fee_price,
                    'product_uom_qty': 1,
                    'qty_delivered': 1,
                    'discount': 0,
                    'company_id': vals['company_id'],
                    'currency_id': 1
                }
                if vals['company_id'] == partner.fee_id.company_id.id:
                    sale_line_data['tax_id'] = [(6, 0, [partner.fee_id.tax_id.id])]
                else:
                    sale_line_data['tax_id'] = [(6, 0, [partner.fee_id.fee_linked.tax_id.id])]
                if vals.get('order_line'):
                    vals['order_line'] += [(0, 0, sale_line_data)]
                else:
                    vals['order_line'] = [(0, 0, sale_line_data)]
        vals['fee_price'] = fee_price
        return super(SaleOrder, self).create(vals)

    @api.multi
    def write(self, values):
        _logger.warning(self)
        _logger.warning(values)
        amount_change = 0
        no_order_line = 0
        if not values.get('order_line', False):
            no_order_line = 1
        if values.get('order_line'):
            for line in values['order_line']:
                if line[0] == 0:
                    amount_change += line[2]['product_uom_qty'] * (
                                line[2]['price_unit'] * (1 - (line[2]['discount'] or 0.0) / 100))
                elif line[0] == 2:
                    amount_change -= self.env['sale.order.line'].search([('id', '=', line[1])])['price_subtotal']
                elif line[0] == 1 and 'product_uom_qty' in line[2]:
                    amount_change -= (line[2]['product_uom_qty'] - self.env['sale.order.line'].browse(line[1])[
                                         'product_uom_qty']) * (
                                                 line[2]['price_unit'] * (1 - (line[2]['discount'] or 0.0) / 100))

        if ('apply_fee' not in values and not self.apply_fee) or ('apply_fee' in values and not values['apply_fee']):
            fee_price = 0
        else:
            if self.company_id.id == self.partner_id.fee_id.company_id.id:
                fee_line = self.partner_id.fee_id._check_condition_to_apply(self.amount_untaxed + amount_change)
            else:
                fee_line = self.partner_id.fee_id.fee_linked._check_condition_to_apply(self.amount_untaxed + amount_change)
            if fee_line:
                if fee_line.value_type == 'perc':
                    fee_price = self.amount_untaxed * fee_line.value_apply / 100
                elif fee_line.value_type == 'fix':
                    fee_price = fee_line.value_apply
            else:
                fee_price = 0
        if self.fee_price != fee_price:
            product_fee = self.env['product.product'].search([('fee_product', '=', True)])
            billing_line = self.env['sale.order.line'].search(
                [('order_id', '=', self.id), ('product_id', '=', product_fee.id)])
            if billing_line:
                sale_line_data = {
                    'price_unit': fee_price
                }
                if values.get('order_line'):
                    values['order_line'] += [(1, billing_line.id, sale_line_data)]
                else:
                    values['order_line'] = [(1, billing_line.id, sale_line_data)]
                # sale_line_data = {
                #     'price_unit': fee_price,
                #     'price_subtotal': fee_price,
                #     'price_total': fee_price,
                #     'price_subtotal_signed': fee_price,
                # }
            else:
                sale_line_data = {
                    'name': 'Billing Fee',
                    'product_id': self.env.ref('hodei_billing_fees.product_fees').id,
                    'price_unit': fee_price,
                    'price_subtotal': fee_price,
                    'price_total': fee_price,
                    'product_uom_qty': 1,
                    'qty_delivered': 1,
                    'discount': 0,
                    'company_id': self.company_id.id,
                    'currency_id': 1
                }
                if self.company_id.id == self.partner_id.fee_id.company_id.id:
                    sale_line_data['tax_id'] = [(6, 0, [self.partner_id.fee_id.tax_id.id])]
                else:
                    sale_line_data['tax_id'] = [(6, 0, [self.partner_id.fee_id.fee_linked.tax_id.id])]
                if sale_line_data:
                    if values.get('order_line'):
                        values['order_line'] += [(0, 0, sale_line_data)]
                    else:
                        values['order_line'] = [(0, 0, sale_line_data)]
            values['fee_price'] = fee_price
            if 'order_line' in values:
                line_to_delete = False
                for x in range(len(values['order_line'])):
                    if values['order_line'][x][1] == billing_line.id:
                        if values['order_line'][x][2]:
                            values['order_line'][x][2]['price_unit'] = fee_price
                        else:
                            line_to_delete = x
                if line_to_delete:
                    del values['order_line'][line_to_delete]
            else:
                values['order_line'] = [1, billing_line.id, {'price_unit': fee_price}]
            if no_order_line == 1:
                lines = self.env['sale.order.line'].search(
                    [('order_id', '=', self.id), ('product_id', '!=', product_fee.id)])
                for line in lines:
                    values['order_line'] += [[4, line.id, False]]
        _logger.warning(values)
        return super(SaleOrder, self).write(values)

    @api.depends('invoice_lines.invoice_id.state', 'invoice_lines.quantity')
    def _get_invoice_qty(self):
        super(SaleOrder, self)._get_invoice_qty()
        for line in self:
            _logger.warning(line.product_id)
            _logger.warning(self.env.ref('hodei_billing_fees.product_fees').id)
            if line.product_id == self.env.ref('hodei_billing_fees.product_fees').id:
                _logger.warning("oui")
                line.qty_invoiced = 1

    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        res['apply_fee'] = self.apply_fee
        return res
