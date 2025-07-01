# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class vit_hr_pendidikan(models.Model):
#     _name = 'vit_hr_pendidikan.vit_hr_pendidikan'
#     _description = 'vit_hr_pendidikan.vit_hr_pendidikan'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
