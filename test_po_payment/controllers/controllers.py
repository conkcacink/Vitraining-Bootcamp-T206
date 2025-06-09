# -*- coding: utf-8 -*-
# from odoo import http


# class TestPoPayment(http.Controller):
#     @http.route('/test_po_payment/test_po_payment', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/test_po_payment/test_po_payment/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('test_po_payment.listing', {
#             'root': '/test_po_payment/test_po_payment',
#             'objects': http.request.env['test_po_payment.test_po_payment'].search([]),
#         })

#     @http.route('/test_po_payment/test_po_payment/objects/<model("test_po_payment.test_po_payment"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('test_po_payment.object', {
#             'object': obj
#         })
