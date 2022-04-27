# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

# mapping invoice type to refund type
TYPE2REFUND = {
    'out_invoice': 'out_refund',        # Customer Invoice
    'in_invoice': 'in_refund',          # Vendor Bill
    'out_refund': 'out_invoice',        # Customer Credit Note
    'in_refund': 'in_invoice',          # Vendor Credit Note
}

MAGIC_COLUMNS = ('id', 'create_uid', 'create_date', 'write_uid', 'write_date')


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    fee_price = fields.Float('Billing Fee', store=True, default="0")
    apply_fee = fields.Boolean(string='Apply Fee', default=True)

    @api.model
    def create(self, vals):
        if type == 'out_refund':
            vals.apply_fee = False
        else:
            amount_change = 0
            if vals.get('invoice_line_ids'):
                for line in vals['invoice_line_ids']:
                    _logger.warning(line[0])
                    if line[0] == 0:
                        if not 'discount' in line[2] or line[2]['discount'] == 0:
                            amount_change += line[2]['quantity'] * line[2]['price_unit']
                        else:
                            amount_change += line[2]['quantity'] * line[2]['price_unit'] * line[2]['discount']/100
                        _logger.warning(amount_change)
                    elif line[0] == 2:
                        amount_change -= self.env['account.invoice.line'].search([('id', '=', line[1])])['price_subtotal']
            _logger.warning('_________________amount_change')
            _logger.warning(amount_change)
            _logger.warning(vals['partner_id'])
            if vals.get('apply_fee'):
                partner = self.env['res.partner'].search([('id', '=', vals['partner_id'])])
                if self.company_id.id == partner.fee_id.company_id.id:
                    fee_line = partner.fee_id._check_condition_to_apply(amount_change)
                else:
                    fee_line = partner.fee_id.fee_linked._check_condition_to_apply(amount_change)
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
                invoice_line_data = {
                    'name': 'Billing Fee',
                    'product_id': self.env.ref('hodei_billing_fees.product_fees').id,
                    'uom_id': 1,
                    'partner_id': partner.id,
                    'price_unit': fee_price,
                    'quantity': 1,
                    'discount': 0,
                    'company_id': vals['company_id'],
                    'currency_id': 1
                }
                _logger.warning(vals)
                _logger.warning('_______________debut')
                _logger.warning(vals['company_id'])
                _logger.warning(partner.fee_id.company_id.id)
                if vals['company_id'] == partner.fee_id.company_id.id:
                    invoice_line_data['account_id'] = partner.fee_id.account_id.id
                    invoice_line_data['invoice_line_tax_ids'] = [(6, False, [partner.fee_id.tax_id.id])]
                else:
                    invoice_line_data['account_id'] = partner.fee_id.fee_linked.account_id.id
                    invoice_line_data['invoice_line_tax_ids'] = [(6, False, [partner.fee_id.fee_linked.tax_id.id])]
                _logger.warning(invoice_line_data['account_id'])
                _logger.warning(invoice_line_data['invoice_line_tax_ids'])
                if vals.get('invoice_line_ids'):
                    vals['invoice_line_ids'] += [(0, 0, invoice_line_data)]
                else:
                    vals['invoice_line_ids'] = [(0, 0, invoice_line_data)]
            #invoice.compute_taxes()
            vals['fee_price'] = fee_price
        _logger.warning(vals)
        invoice = super(AccountInvoice, self).create(vals)
        invoice.compute_taxes()
        return invoice

    @api.multi
    def write(self, values):
        _logger.warning(values)
        if values.get('type') == 'out_refund':
            values['apply_fee'] = False
        elif 'type' in self and (self.type != 'out_refund' or values['apply_fee']):
            for order in self:
                amount_change = 0
                if values.get('invoice_line_ids'):
                    for line in values['invoice_line_ids']:
                        _logger.warning(line[0])
                        if line[0] == 0:
                            if not 'discount' in line[2] or line[2]['discount'] == 0:
                                amount_change += line[2]['quantity'] * line[2]['price_unit']
                            else:
                                amount_change += line[2]['quantity'] * line[2]['price_unit'] * line[2]['discount'] / 100
                            _logger.warning(amount_change)
                        elif line[0] == 2:
                            amount_change -= self.env['account.invoice.line'].search([('id', '=', line[1])])['price_subtotal']
                            _logger.warning(amount_change)
                    _logger.warning('_________________amount_change')
                    _logger.warning(amount_change)
                if ('apply_fee' not in values and not order.apply_fee) or ('apply_fee' in values and not values['apply_fee']):
                    fee_price = 0
                else:
                    if order.company_id.id == order.partner_id.fee_id.company_id.id:
                        fee_line = order.partner_id.fee_id._check_condition_to_apply(order.amount_untaxed + amount_change)
                    else:
                        fee_line = order.partner_id.fee_id.fee_linked._check_condition_to_apply(order.amount_untaxed + amount_change)
                    if fee_line:
                        if fee_line.value_type == 'perc':
                            fee_price = order.amount_untaxed * fee_line.value_apply / 100
                        elif fee_line.value_type == 'fix':
                            fee_price = fee_line.value_apply
                    else:
                        fee_price = 0
                _logger.warning(order.fee_price)
                _logger.warning('_________________fee_price')
                _logger.warning(fee_price)
                if order.fee_price != fee_price:
                    product_fee = self.env['product.product'].search([('fee_product', '=', True)])
                    billing_line = self.env['account.invoice.line'].search(
                        [('invoice_id', '=', order.id), ('product_id', '=', product_fee.id)])
                    _logger.warning('_________________billing_line')
                    _logger.warning(billing_line)
                    if billing_line:
                        invoice_line_data = {
                            'price_unit': fee_price
                        }
                        if values.get('invoice_line_ids'):
                            values['invoice_line_ids'] += [(1, billing_line.id, invoice_line_data)]
                        else:
                            values['invoice_line_ids'] = [(1, billing_line.id, invoice_line_data)]
                            _logger.warning('invoice_line_data')
                            _logger.warning(invoice_line_data)
                        if fee_price == 0:
                            if values.get('tax_line_ids'):
                                values['tax_line_ids'][0][2]['amount'] -= order.fee_price * order.partner_id.fee_id.tax_id.amount
                            else:
                                tax_line = self.env['account.invoice.tax'].search(
                                    [('id', 'in', order.tax_line_ids.ids), ('tax_id', '=', order.partner_id.fee_id.tax_id.id)])
                                tax_line.write({'amount': tax_line['amount'] - order.fee_price * order.partner_id.fee_id.tax_id.amount/100})
                        else:
                            tax_line = self.env['account.invoice.tax'].search(
                                [('id', 'in', order.tax_line_ids.ids), ('tax_id', '=', order.partner_id.fee_id.tax_id.id)])
                            tax_line.write({'amount': tax_line['amount'] + fee_price * order.partner_id.fee_id.tax_id.amount/100 - order.fee_price * order.partner_id.fee_id.tax_id.amount / 100})
                    else:
                        _logger.warning('add________________________')
                        invoice_line_data = {
                            'name': 'Billing Fee',
                            'product_id': self.env.ref('hodei_billing_fees.product_fees').id,
                            'uom_id': 1,
                            'origin': order.origin,
                            'invoice_id': order.id,
                            'partner_id': order.partner_id.id,
                            'price_unit': fee_price,
                            'price_subtotal': fee_price,
                            'price_total': fee_price,
                            'price_subtotal_signed': fee_price,
                            'quantity': 1,
                            'discount': 0,
                            'company_id': order.company_id.id,
                            'currency_id': 1
                        }
                        _logger.warning(order.company_id.id)
                        if order.company_id.id == order.partner_id.fee_id.company_id.id:
                            invoice_line_data['account_id'] = order.partner_id.fee_id.account_id.id
                            invoice_line_data['invoice_line_tax_ids'] = [(6, 0, [order.partner_id.fee_id.tax_id.id])]
                        else:
                            invoice_line_data['account_id'] = order.partner_id.fee_id.fee_linked.account_id.id
                            invoice_line_data['invoice_line_tax_ids'] = [(6, 0, [order.partner_id.fee_id.fee_linked.tax_id.id])]
                        if invoice_line_data:
                            if values.get('invoice_line_ids'):
                                values['invoice_line_ids'] += [(0, 0, invoice_line_data)]
                            else:
                                values['invoice_line_ids'] = [(0, 0, invoice_line_data)]
                            if values.get('tax_line_ids'):
                                values['tax_line_ids'][0][2]['amount'] += fee_price * 20/100
                    values['fee_price'] = fee_price
                    _logger.warning(values)
                    return super(AccountInvoice, order).write(values)
        return super(AccountInvoice, self).write(values)

    @api.model
    def _refund_cleanup_lines(self, lines):
        """ Convert records to dict of values suitable for one2many line creation

            :param recordset lines: records to convert
            :return: list of command tuple for one2many line creation [(0, 0, dict of valueis), ...]
        """
        result = []
        for line in lines:
            values = {}
            product_fee = self.env['product.product'].search([('fee_product', '=', True)])
            _logger.warning('line______________________________')
            _logger.warning(line)
            if 'product_id' in line and line['product_id'].id == product_fee.id:
                continue
            for name, field in line._fields.items():
                if name in MAGIC_COLUMNS:
                    continue
                elif field.type == 'many2one':
                    values[name] = line[name].id
                elif field.type not in ['many2many', 'one2many']:
                    values[name] = line[name]
                elif name == 'invoice_line_tax_ids':
                    values[name] = [(6, 0, line[name].ids)]
                elif name == 'analytic_tag_ids':
                    values[name] = [(6, 0, line[name].ids)]
            result.append((0, 0, values))

        return result

    @api.model
    def _prepare_refund(self, invoice, date_invoice=None, date=None, description=None, journal_id=None):
        values = super(AccountInvoice, self)._prepare_refund(invoice, date_invoice, date, description, journal_id)
        values['apply_fee'] = False
        return values


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    @api.model_create_multi
    def create(self, vals_list):
        _logger.warning('vals_list__________________')
        for vals in vals_list:
            if vals['product_id'] == self.env.ref('hodei_billing_fees.product_fees')['id']:
                invoice = self.env['account.invoice'].search([('id', '=', vals['invoice_id'])])
                for line in invoice.invoice_line_ids:
                    if line['product_id'] == self.env.ref('hodei_billing_fees.product_fees'):
                        vals_list.remove(vals)
        _logger.warning(vals_list)

        return super(AccountInvoiceLine, self).create(vals_list)

class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    @api.multi
    def create_invoices(self):
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))

        if self.advance_payment_method == 'delivered':
            _logger.warning('delivered__________________')
            sale_orders.action_invoice_create()
        elif self.advance_payment_method == 'all':
            _logger.warning('all________________________')
            sale_orders.action_invoice_create(final=True)
        else:
            _logger.warning('else________________________')
            # Create deposit product if necessary
            if not self.product_id:
                vals = self._prepare_deposit_product()
                self.product_id = self.env['product.product'].create(vals)
                self.env['ir.config_parameter'].sudo().set_param('sale.default_deposit_product_id', self.product_id.id)

            sale_line_obj = self.env['sale.order.line']
            _logger.warning('sale_line_obj________________________')
            _logger.warning(sale_line_obj)
            for order in sale_orders:
                if self.advance_payment_method == 'percentage':
                    amount = order.amount_untaxed * self.amount / 100
                else:
                    amount = self.amount
                if self.product_id.invoice_policy != 'order':
                    raise UserError(_('The product used to invoice a down payment should have an invoice policy set to "Ordered quantities". Please update your deposit product to be able to create a deposit invoice.'))
                if self.product_id.type != 'service':
                    raise UserError(_("The product used to invoice a down payment should be of type 'Service'. Please use another product or update this product."))
                taxes = self.product_id.taxes_id.filtered(lambda r: not order.company_id or r.company_id == order.company_id)
                if order.fiscal_position_id and taxes:
                    tax_ids = order.fiscal_position_id.map_tax(taxes, self.product_id, order.partner_shipping_id).ids
                else:
                    tax_ids = taxes.ids
                context = {'lang': order.partner_id.lang}
                analytic_tag_ids = []
                for line in order.order_line:
                    analytic_tag_ids = [(4, analytic_tag.id, None) for analytic_tag in line.analytic_tag_ids]
                so_line = sale_line_obj.create({
                    'name': _('Advance: %s') % (time.strftime('%m %Y'),),
                    'price_unit': amount,
                    'product_uom_qty': 0.0,
                    'order_id': order.id,
                    'discount': 0.0,
                    'product_uom': self.product_id.uom_id.id,
                    'product_id': self.product_id.id,
                    'analytic_tag_ids': analytic_tag_ids,
                    'tax_id': [(6, 0, tax_ids)],
                    'is_downpayment': True,
                })
                del context
                self._create_invoice(order, so_line, amount)
        if self._context.get('open_invoices', False):
            return sale_orders.action_view_invoice()
        return {'type': 'ir.actions.act_window_close'}
