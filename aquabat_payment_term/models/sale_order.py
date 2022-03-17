# -*- coding: utf-8 -*-

from odoo import fields, models, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    payment_term_id = fields.Many2one('account.payment.term', string='Payment Terms', check_company=True, 
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")

    def action_confirm(self):
        if self.payment_term_id:
            return super(SaleOrder, self).action_confirm()
        else:
            raise UserError(_('It is not allowed to confirm an order without any account payment term.'))
