from odoo import models, fields, api

class Partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    
    kota_id = fields.Many2one("vit.kota", string="Kota")