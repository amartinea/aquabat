# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    billable_total = fields.Float('Billable Total', readonly=True)
    billable_marge = fields.Float('Billable Marge', readonly=True)
    #percent_billable_marge = fields.Float('Billable % Marge', readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['billable_total'] = ", sum(l.price_reduce_taxexcl * l.qty_delivered / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) as billable_total"
        fields['billable_marge'] = ', sum((l.price_reduce_taxexcl - l.purchase_price) * l.qty_delivered / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) as billable_marge'
        #fields['percent_billable_marge'] = ', sum((l.price_reduce_taxexcl - l.purchase_price) * l.qty_delivered) / sum(l.purchase_price) * 100 / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) as percent_billable_marge'

        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)
