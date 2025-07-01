from odoo import models, fields, api, _
from odoo.exceptions import ValidationError # type: ignore

class riwayat_pendidikan(models.Model):
    _name = "vit.riwayat_pendidikan"
    _description = "vit.riwayat_pendidikan"
    
    gelar = fields.Many2one(comodel_name="vit.gelar", required=True, copy=False, string=_("Gelar"))
    tahun_mulai = fields.Char(string=_("Tahun Mulai"), required=True)
    tahun_selesai = fields.Char(string=_("Tahun Selesai"), required=True)
    ipk = fields.Float(string=_("IPK"))
    keterangan = fields.Char(string=_("Keterangan"))
    employee_id = fields.Many2one(comodel_name="hr.employee", string=_("Employee"))
    institusi_id = fields.Many2one(comodel_name="res.partner", string=_("Institusi"), required=True)
    
    @api.constrains('tahun_mulai')
    def _check_tahun_mulai_not_zero(self):
        for record in self:
            if not record.tahun_mulai or record.tahun_mulai == '0':
                raise ValidationError("Field 'Tahun Mulai' tidak boleh kosong atau nol.")
            
    @api.constrains('tahun_selesai')
    def _check_tahun_selesai_not_zero(self):
        for record in self:
            if not record.tahun_selesai or record.tahun_selesai == '0':
                raise ValidationError("Field 'Tahun Selesai' tidak boleh kosong atau nol.")
            
    @api.constrains('ipk')
    def _check_ipk_value(self):
        for record in self:
            if record.ipk == 0.00:
                raise ValidationError("IPK tidak boleh nol.")
            if record.ipk < 2.00:
                raise ValidationError("IPK tidak boleh kurang dari 2.0.")
            
    @api.constrains('tahun_mulai', 'tahun_selesai')
    def _check_tahun_range(self):
        for record in self:
            try:
                tahun_mulai = int(record.tahun_mulai)
                tahun_selesai = int(record.tahun_selesai)

                if tahun_selesai <= tahun_mulai:
                    raise ValidationError(_("Tahun Selesai harus lebih besar dari Tahun Mulai."))

                gap = tahun_selesai - tahun_mulai
                if gap < 2:
                    raise ValidationError(_("Rentang tahun pendidikan minimal 2 tahun."))
                if gap > 5:
                    raise ValidationError(_("Rentang tahun pendidikan maksimal 5 tahun."))
            except ValueError:
                raise ValidationError(_("Tahun Mulai dan Tahun Selesai harus berupa angka tahun yang valid."))