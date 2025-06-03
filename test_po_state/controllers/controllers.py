# -*- coding: utf-8 -*-
# from odoo import http


# class TestPoState(http.Controller):
#     @http.route('/test_po_state/test_po_state', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/test_po_state/test_po_state/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('test_po_state.listing', {
#             'root': '/test_po_state/test_po_state',
#             'objects': http.request.env['test_po_state.test_po_state'].search([]),
#         })

#     @http.route('/test_po_state/test_po_state/objects/<model("test_po_state.test_po_state"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('test_po_state.object', {
#             'object': obj
#         })
