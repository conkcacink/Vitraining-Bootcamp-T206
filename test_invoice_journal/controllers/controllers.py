# -*- coding: utf-8 -*-
# from odoo import http


# class TestInvoiceJournal(http.Controller):
#     @http.route('/test_invoice_journal/test_invoice_journal', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/test_invoice_journal/test_invoice_journal/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('test_invoice_journal.listing', {
#             'root': '/test_invoice_journal/test_invoice_journal',
#             'objects': http.request.env['test_invoice_journal.test_invoice_journal'].search([]),
#         })

#     @http.route('/test_invoice_journal/test_invoice_journal/objects/<model("test_invoice_journal.test_invoice_journal"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('test_invoice_journal.object', {
#             'object': obj
#         })
