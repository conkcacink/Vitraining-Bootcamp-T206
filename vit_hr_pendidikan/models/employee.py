from odoo import models, fields, api, _
class employee(models.Model):
    _name = "hr.employee"
    _inherit = "hr.employee"
    riwayat_pendidikan_ids = fields.One2many(comodel_name="vit.riwayat_pendidikan", inverse_name="employee_id", string=_("Riwayat Pendidikan"))