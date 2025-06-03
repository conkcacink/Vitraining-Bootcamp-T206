# -*- coding: utf-8 -*-
from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    # state = fields.Selection(selection_add = [('verification', 'Verification')])
    state = fields.Selection([
                ('draft', 'Request for Quotation'),
                ('verification', 'Verification'),
                ('sent', 'RFQ Sent'),
                # ('to approve', 'To Approve'),
                ('purchase', 'Purchase Order'),
                # ('done', 'Locked'),
                # ('cancel', 'Cancelled')
            ], string='Status', readonly=True, copy=False, tracking=True, default='draft')
    
    def button_verify(self):
        self.write({'state': 'verification'})
        
    def button_confirm(self):
        for order in self:
            if order.state not in ['draft', 'sent', 'verification']:
                continue
            order.order_line._validate_analytic_distribution()
            order._add_supplier_to_product()
            if order._approval_allowed():
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
            if order.partner_id not in order.message_partner_ids:
                order.message_subscribe([order.partner_id.id])
        return True