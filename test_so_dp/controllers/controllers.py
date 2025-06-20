# -*- coding: utf-8 -*-
# from odoo import http


# class TestSoDp(http.Controller):
#     @http.route('/test_so_dp/test_so_dp', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/test_so_dp/test_so_dp/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('test_so_dp.listing', {
#             'root': '/test_so_dp/test_so_dp',
#             'objects': http.request.env['test_so_dp.test_so_dp'].search([]),
#         })

#     @http.route('/test_so_dp/test_so_dp/objects/<model("test_so_dp.test_so_dp"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('test_so_dp.object', {
#             'object': obj
#         })
