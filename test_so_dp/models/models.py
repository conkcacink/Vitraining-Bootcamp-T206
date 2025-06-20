# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class test_so_dp(models.Model):
#     _name = 'test_so_dp.test_so_dp'
#     _description = 'test_so_dp.test_so_dp'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
