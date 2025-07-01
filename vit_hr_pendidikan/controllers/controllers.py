# -*- coding: utf-8 -*-
# from odoo import http


# class VitHrPendidikan(http.Controller):
#     @http.route('/vit_hr_pendidikan/vit_hr_pendidikan', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_hr_pendidikan/vit_hr_pendidikan/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_hr_pendidikan.listing', {
#             'root': '/vit_hr_pendidikan/vit_hr_pendidikan',
#             'objects': http.request.env['vit_hr_pendidikan.vit_hr_pendidikan'].search([]),
#         })

#     @http.route('/vit_hr_pendidikan/vit_hr_pendidikan/objects/<model("vit_hr_pendidikan.vit_hr_pendidikan"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_hr_pendidikan.object', {
#             'object': obj
#         })
