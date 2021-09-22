# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ResCompany(models.Model):
    _inherit = "res.company"

    company_link_id = fields.Many2one('res.company', string="company linked to display customer", default=False)
