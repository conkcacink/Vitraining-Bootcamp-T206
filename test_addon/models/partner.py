from odoo import models, fields, api

class Partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    
    npwp = fields.Char(string="NPWP", required=True)