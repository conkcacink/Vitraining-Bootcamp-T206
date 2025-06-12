# -*- coding: utf-8 -*-
# from odoo import http


# class TestPoItemDiscount(http.Controller):
#     @http.route('/test_po_item_discount/test_po_item_discount', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/test_po_item_discount/test_po_item_discount/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('test_po_item_discount.listing', {
#             'root': '/test_po_item_discount/test_po_item_discount',
#             'objects': http.request.env['test_po_item_discount.test_po_item_discount'].search([]),
#         })

#     @http.route('/test_po_item_discount/test_po_item_discount/objects/<model("test_po_item_discount.test_po_item_discount"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('test_po_item_discount.object', {
#             'object': obj
#         })
