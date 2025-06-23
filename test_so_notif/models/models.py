# -*- coding: utf-8 -*-

from odoo import models, fields, api

class sale(models.Model):
    _inherit = 'sale.order'
    
    def action_confirm(self):
        res = super(sale, self).action_confirm()
        self.send_notif()
        return res
    
    def send_notif(self):
        recipient_id = self.create_uid.partner_id.id
        channel = self.env['mail.channel'].channel_get([recipient_id])
        
        user_id = self.env.user.id
        message = ("Your Sales Order %s has been validated.") % (self.name)
        
        channel_id = self.env['mail.channel'].browse(channel["id"])
        channel_id.message_notify(
            author_id = user_id,
            partner_ids = [recipient_id],
            subject = "Information",
            body = (message),
            message_type = 'comment',
            subtype_xmlid = "mail.mt_note",
            notify_by_email = False,
        )