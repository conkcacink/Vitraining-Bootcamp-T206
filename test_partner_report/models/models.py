from odoo import models, fields, api
import xlwt
import base64
from io import BytesIO


class test_partner_report(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    bank_account_ids = fields.One2many(
        'res.partner.bank', 'partner_id', string='Bank Accounts')

    def print_customer_card(self):
        return self.env.ref('test_partner_report.action_report_customer_card').report_action(self)

    def export_partner_to_excel(self):
        # pass
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet("Partners")

        worksheet.write(0, 0, "Name")
        worksheet.write(0, 1, self.name or '')

        worksheet.write(0, 3, "Email")
        worksheet.write(0, 4, self.email or '')

        worksheet.write(1, 0, "Phone")
        worksheet.write(1, 1, self.phone or '')

        row = 5

        worksheet.write(row, 0, "Contacts")

        row += 1

        worksheet.write(row, 0, "Name")
        worksheet.write(row, 1, "Email")
        worksheet.write(row, 2, "Phone")

        row += 1

        for contact in self.child_ids:
            worksheet.write(row, 0, contact.name)
            worksheet.write(row, 1, contact.email)
            worksheet.write(row, 2, contact.phone)
            row += 1

        # bank account data
        row += 1
        worksheet.write(row, 0, "Bank Account")
        row += 1
        worksheet.write(row, 0, "Name")
        worksheet.write(row, 1, "Number")
        worksheet.write(row, 2, "Holder")
        row += 1
        for account in self.bank_account_ids:
            worksheet.write(row, 0, account.bank_id.name)
            worksheet.write(row, 1, account.acc_number)
            worksheet.write(row, 2, account.partner_id.name)
            row += 1

        # save workbook
        buffer = BytesIO()
        workbook.save(buffer)
        file_data = base64.b64encode(buffer.getvalue())
        
        attachment = {
            'name': 'partners.xls',
            'datas': file_data, #base64
            'res_model': 'res.partner',
            'res_id': self.ids[0],
            'type': 'binary'
        }
        attachment_id = self.env['ir.attachment'].create(attachment)
        
        return{
            'type': 'ir.actions.act_url',
            'url': '/web/content/%d?download=true' % attachment_id.id,
            'target': 'self'
        }

#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
