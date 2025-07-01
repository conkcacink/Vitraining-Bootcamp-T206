from odoo import models, fields, api, _
class level(models.Model):
    _name = "vit.level"
    name = fields.Char(required=True, copy=False, strings=_("Name"))