from odoo import models, fields, api

class AccountMoveInherited(models.Model):
    _inherit = 'account.move'
    
    @api.model
    def create(self, vals):
        move = super(AccountMoveInherited, self).create(vals)
        if move.move_type == 'out_invoice':
            self._modify_journal_entry(move)
        
        return move
    
    def _modify_journal_entry(self, move):
        debit_value = 1000.0
        credit_value = 1000.0
        account_debit = self.env['account.account'].search([('code', '=', '961000')], limit=1)
        account_credit  = self.env['account.account'].search([('code', '=', '101501')], limit=1)
        
        base_amount = sum(move.invoice_line_ids.mapped('price_subtotal'))
        adjustment_value = base_amount * 0.05
        
        if account_debit and account_credit:
            vals_debit = {
                'account_id' : account_debit.id,
                # 'debit' : debit_value,
                'debit' : adjustment_value,
                'credit' : 0.0,
                'display_type' : 'tax',
                'name': 'R&D Adjustment (5%)',
            }
            vals_credit = {
                'account_id' : account_credit.id,
                'debit' : 0.0,
                # 'credit' : credit_value,
                'credit' : adjustment_value,
                'display_type' : 'tax',
                'name': 'Cash Adjustment (5%)',
            }
            move.write({
                'line_ids' : [(0,0,vals_debit),(0,0,vals_credit)]
            })