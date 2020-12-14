# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp
from odoo.tools.float_utils import float_round


class ProductProduct(models.Model):
    _inherit = "product.product"

    qty_real_available = fields.Float('Real Forecast Quantity', compute='_compute_quantities')

    @api.depends('stock_move_ids.product_qty', 'stock_move_ids.state')
    def _compute_quantities(self):
        res = self._compute_quantities_dict(self._context.get('lot_id'), self._context.get('owner_id'), self._context.get('package_id'), self._context.get('from_date'), self._context.get('to_date'))
        for product in self:
            product.qty_available = res[product.id]['qty_available']
            product.incoming_qty = res[product.id]['incoming_qty']
            product.outgoing_qty = res[product.id]['outgoing_qty']
            product.virtual_available = res[product.id]['virtual_available']
            product.qty_real_available = res[product.id]['virtual_available'] - res[product.id]['incoming_qty']


    def _compute_quantities_dict_by_company(self, company_id):
        
        #define domain quant
        Quant = self.env['stock.quant']
        domain_quant_loc, domain_move_in_loc, domain_move_out_loc = self._get_domain_locations()
        domain_quant = [('product_id', 'in', self.ids)] + domain_quant_loc

        #define domain move out
        Move = self.env['stock.move']
        domain_move_out = [('product_id', 'in', self.ids)] + domain_move_out_loc
        domain_move_out_todo = [('state', 'in', ('waiting', 'confirmed', 'assigned', 'partially_available'))] + domain_move_out

        if company_id is not None:
            domain_quant += [('company_id', '=', company_id)]
            domain_move_out_todo += [('company_id', '=', company_id)]
        for product in self.with_context(prefetch_fields=False):
            product_id = product.id
            rounding = product.uom_id.rounding
            #calcul quant
            quants_res = dict((item['product_id'][0], item['quantity']) for item in Quant.read_group(domain_quant, ['product_id', 'quantity'], ['product_id'], orderby='id'))
            qty_available = float_round(quants_res.get(product_id, 0.0), precision_rounding=rounding)

            #calcul move out
            moves_out_res = dict((item['product_id'][0], item['product_qty']) for item in Move.read_group(domain_move_out_todo, ['product_id', 'product_qty'], ['product_id'], orderby='id'))
            outgoing_qty = float_round(moves_out_res.get(product_id, 0.0), precision_rounding=rounding)

            qty_real_available = qty_available - outgoing_qty

        return float_round(qty_real_available, precision_rounding=rounding)
