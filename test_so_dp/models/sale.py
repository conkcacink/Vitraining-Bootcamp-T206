from odoo import api, fields, models
from odoo.tools import float_compare

class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    account_payment_ids = fields.One2many('account.payment', 'sale_id', string="Pay Advanced Sales")
    
    amount_residual = fields.Float(
        "Residual Amount", readonly=True, compute="_compute_advance_payment", store=True,
    )
    
    payment_line_ids = fields.Many2many(
        "account.move.line", string="Payment Move Lines", compute="_compute_advance_payment",store=True,
    )
    
    advance_payment_status = fields.Selection(
        selection = [
            ("not_paid", "Not Paid"),
            ("paid", "Paid"),
            ("partial", "Partially Paid")  
        ],
        store = True,
        readonly = True,
        copy = False,
        tracking = True,
        compute = "_compute_advance_payment",
    )
    
    @api.depends(
        "currency_id",
        "amount_total",
        "account_payment_ids",
        "account_payment_ids.state",
        "account_payment_ids.move_id",
        "account_payment_ids.move_id.line_ids",
        "account_payment_ids.move_id.line_ids.date",
        "account_payment_ids.move_id.line_ids.debit",
        "account_payment_ids.move_id.line_ids.credit",
        "account_payment_ids.move_id.line_ids.currency_id",
        "account_payment_ids.move_id.line_ids.amount_currency",
        "invoice_ids.amount_residual",
    )
    def _compute_advance_payment(self):
        # pass
        for order in self:
            mls = order.account_payment_ids.mapped("move_id.line_ids").filtered(
                lambda x: x.account_id.account_type == "asset_receivable" and x.parent_state == "posted"
            )
            advance_amount = 0.0
            for line in mls:
                line_currency = line.currency_id or line.company_id.currency_id
                line_amount = (
                    line.amount_residual_currency
                    if line.currency_id
                    else line.amount_residual
                )
                line_amount *= -1
                if line_currency != order.currency_id:
                    advance_amount += line.currency_id._convert(
                        line_amount,
                        order.currency_id,
                        order.company_id,
                        line.date or fields.Date.today(),
                    )
                else:
                    advance_amount += line_amount
                    
            invoice_paid_amount = 0.0
            
            for inv in order.invoice_ids:
                invoice_paid_amount += inv.amount_total - inv.amount_residual
            
            amount_residual = order.amount_total - advance_amount - invoice_paid_amount
            
            payment_state = "not_paid"
            
            if mls:
                has_due_amount = float_compare(
                    amount_residual, 0.0, precision_rounding = order.currency_id.rounding
                )
                if has_due_amount <= 0:
                    payment_state = "paid"
                elif has_due_amount > 0:
                    payment_state = "partial"
            
            order.payment_line_ids = mls
            order.amount_residual = amount_residual
            order.advance_payment_status = payment_state