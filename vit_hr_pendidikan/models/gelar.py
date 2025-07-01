from odoo import models, fields, api, _

class gelar(models.Model):
    _name = "vit.gelar"
    _description = "vit.gelar"
    
    name = fields.Char(required=True, copy=False, string=_("Name"))
    level_id = fields.Many2one(comodel_name="vit.level", string=_("Level"))