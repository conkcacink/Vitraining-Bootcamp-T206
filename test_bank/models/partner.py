from odoo import models, fields, api

class Partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    
    bank_account_ids = fields.One2many(
        comodel_name = 'res.partner.bank',
        inverse_name = 'partner_id',
        string = "Bank Accounts"
    )