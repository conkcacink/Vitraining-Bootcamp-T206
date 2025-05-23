# -*- coding: utf-8 -*-
# from odoo import http


# class TestPartnerReport(http.Controller):
#     @http.route('/test_partner_report/test_partner_report', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/test_partner_report/test_partner_report/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('test_partner_report.listing', {
#             'root': '/test_partner_report/test_partner_report',
#             'objects': http.request.env['test_partner_report.test_partner_report'].search([]),
#         })

#     @http.route('/test_partner_report/test_partner_report/objects/<model("test_partner_report.test_partner_report"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('test_partner_report.object', {
#             'object': obj
#         })
