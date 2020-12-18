# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class StockRoute(models.Model):
    _inherit = "stock.location.route"

    default_route = fields.Boolean(string="Route par défaut")
    # default_update_route = fields.Boolean(string="Seconde route par défaut")

    @api.onchange('default_route')
    def on_default_route(self):
        # Check if an other default_route is set for this company
        if self['default_route']:
            already_set = self.env['stock.location.route'].search([('default_route', '=', True), ('company_id', '=', self['company_id'].id)])
            if already_set:
                raise UserError(_('An other defaut route is set to be the default one : %s') % already_set.name)
            else:
                self.default_route = True

    # @api.onchange('default_update_route')
    # def on_default_update_route(self):
    #     # Check if an other default_update_route is set for this company
    #     if self['default_update_route']:
    #         already_set = self.env['stock.location.route'].search([('default_update_route', '=', True), ('company_id', '=', self['company_id'].id)])
    #         if already_set:
    #             raise UserError(_('An other second defaut route is set to be the default one : %s') % already_set.name)
    #         else:
    #             self.default_update_route = True

    def write(self, vals):
        if 'default_route' in vals and vals['default_route']:
            if vals['default_route'] == True:
                # Check if an other default_route is set
                already_set_default = self.env['stock.location.route'].search([('default_route', '=', True), ('company_id', '=', self['company_id'].id)])
                if already_set_default:
                    raise UserError(_('An other default route is set to be the default one : %s') % already_set_default.name)
                    vals['default_route'] = False
        # if 'default_update_route' in vals and vals['default_update_route']:
        #     if vals['default_update_route'] == True:
        #         # Check if an other default_update_route is set
        #         already_set_update_default = self.env['stock.location.route'].search([('default_update_route', '=', True), ('company_id', '=', self['company_id'].id)])
        #         if already_set_update_default:
        #             raise UserError(_('An other second default route is set to be the default one : %s') % already_set_update_default.name)
        #             vals['default_update_route'] = False
        return super(StockRoute, self).write(vals)
