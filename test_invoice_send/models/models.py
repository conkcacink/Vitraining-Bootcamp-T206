from odoo import models
import logging

_logger = logging.getLogger(__name__)

class test_invoice_send(models.Model):
    __name = 'account.move'
    _inherit = 'account.move'

    def action_post(self):
        res = super().action_post()
        self.action_send_email()
        return res

    def action_send_email(self):
        template = self.env.ref('test_invoice_send.email_notif_post')
        if not template:
            _logger.error("Email template 'email_notif_post' not found!")
            return
        for record in self:
            _logger.info(f"Sending email for invoice: {record.name}")
            template.send_mail(record.id, force_send=True, email_layout_xmlid=None)
