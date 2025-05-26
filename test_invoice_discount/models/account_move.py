from odoo import models, fields, api
from odoo.tools import float_round

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    discount_fixed = fields.Monetary(
        string="Discount (Fixed)",
        default=0.0,
        currency_field="currency_id"
    )

    @api.onchange("discount_fixed")
    def _onchange_discount_fixed(self):
        if self.price_unit and self.quantity:
            base = self.price_unit * self.quantity
            if base:
                self.discount = round((self.discount_fixed / base) * 100, 2)
            else:
                self.discount = 0.0
        else:
            self.discount = 0.0

    @api.onchange("discount")
    def _onchange_discount(self):
        if self.price_unit and self.quantity:
            base = self.price_unit * self.quantity
            self.discount_fixed = round((self.discount / 100.0) * base, 2)
        else:
            self.discount_fixed = 0.0

class AccountMove(models.Model):
    _inherit = "account.move"

    def _recompute_tax_lines(self, recompute_tax_base_amount=False):
        super()._recompute_tax_lines(recompute_tax_base_amount=recompute_tax_base_amount)
        for line in self.invoice_line_ids:
            if line.discount_fixed:
                base = line.price_unit * line.quantity
                subtotal = base - line.discount_fixed
                subtotal_rounded = float_round(subtotal, precision_rounding=line.currency_id.rounding)
                line.price_subtotal = subtotal_rounded
                line.price_total = subtotal_rounded
