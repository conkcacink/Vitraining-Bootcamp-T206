# -*- coding: utf-8 -*-
# from odoo import http


# class TestInvoiceGlobal(http.Controller):
#     @http.route('/test_invoice_global/test_invoice_global', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/test_invoice_global/test_invoice_global/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('test_invoice_global.listing', {
#             'root': '/test_invoice_global/test_invoice_global',
#             'objects': http.request.env['test_invoice_global.test_invoice_global'].search([]),
#         })

#     @http.route('/test_invoice_global/test_invoice_global/objects/<model("test_invoice_global.test_invoice_global"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('test_invoice_global.object', {
#             'object': obj
#         })
