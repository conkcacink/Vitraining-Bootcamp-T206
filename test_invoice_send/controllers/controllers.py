# -*- coding: utf-8 -*-
# from odoo import http


# class TestInvoiceSend(http.Controller):
#     @http.route('/test_invoice_send/test_invoice_send', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/test_invoice_send/test_invoice_send/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('test_invoice_send.listing', {
#             'root': '/test_invoice_send/test_invoice_send',
#             'objects': http.request.env['test_invoice_send.test_invoice_send'].search([]),
#         })

#     @http.route('/test_invoice_send/test_invoice_send/objects/<model("test_invoice_send.test_invoice_send"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('test_invoice_send.object', {
#             'object': obj
#         })
