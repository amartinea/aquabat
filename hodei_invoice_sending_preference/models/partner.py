# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    sending_preference = fields.Selection([('none', ' '),('mail', 'Mail'),('postal', 'Postal')], 
    	string='Invoice Sending Preference', default='none')
