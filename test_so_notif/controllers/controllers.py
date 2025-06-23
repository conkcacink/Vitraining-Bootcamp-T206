# -*- coding: utf-8 -*-
# from odoo import http


# class TestSoNotif(http.Controller):
#     @http.route('/test_so_notif/test_so_notif', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/test_so_notif/test_so_notif/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('test_so_notif.listing', {
#             'root': '/test_so_notif/test_so_notif',
#             'objects': http.request.env['test_so_notif.test_so_notif'].search([]),
#         })

#     @http.route('/test_so_notif/test_so_notif/objects/<model("test_so_notif.test_so_notif"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('test_so_notif.object', {
#             'object': obj
#         })
