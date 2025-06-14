from odoo import fields, models

class ResPartner(models.Model):
    _inherit = "res.partner"
    
    purchase_general_discount = fields.Float(
        digits = "Discounts",
        string = "Purchase General Discount (%)",
        company_dependent = True,
    )