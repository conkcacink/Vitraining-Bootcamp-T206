from odoo import models, fields, api, _

class Institusi(models.Model):
    _name = "res.partner"
    _inherit = "res.partner"
    is_institusi = fields.Boolean(string=_("Is Institusi"))