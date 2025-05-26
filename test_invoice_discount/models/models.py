from odoo import models, fields, api
from odoo.tools import float_is_zero, float_round
from odoo.exceptions import ValidationError

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    discount_fixed = fields.Monetary(
        string="Discount (Fixed)",
        default=0.0,
        currency_field="currency_id"
    )

    @api.onchange("discount_fixed")
    def _onchange_discount_fixed(self):
        if self.env.context.get("ignore_discount_onchange"):
            return
        self.env.context = self.with_context(ignore_discount_onchange=True).env.context

        if self.price_unit and self.quantity:
            base = self.price_unit * self.quantity
            self.discount = round((self.discount_fixed / base) * 100, 2) if base else 0.0
        else:
            self.discount = 0.0

    @api.onchange("discount")
    def _onchange_discount(self):
        if self.env.context.get("ignore_discount_onchange"):
            return
        self.env.context = self.with_context(ignore_discount_onchange=True).env.context

        if self.price_unit and self.quantity:
            base = self.price_unit * self.quantity
            self.discount_fixed = round((self.discount / 100.0) * base, 2)
        else:
            self.discount_fixed = 0.0

    def write(self, vals):
        # Prevent infinite recursion
        if self.env.context.get('skip_custom_write'):
            return super().write(vals)

        # Prepare updated values and compute new subtotal
        lines_to_update = self.filtered(lambda l: l.display_type == 'product')
        new_vals = dict(vals)

        for line in lines_to_update:
            price_unit = new_vals.get('price_unit', line.price_unit)
            quantity = new_vals.get('quantity', line.quantity)
            discount_fixed = new_vals.get('discount_fixed', line.discount_fixed)
            currency = line.currency_id or line.company_id.currency_id

            base = price_unit * quantity
            subtotal = max(base - discount_fixed, 0.0)
            subtotal_rounded = float_round(subtotal, precision_rounding=currency.rounding)

            new_vals['price_subtotal'] = subtotal_rounded
            new_vals['price_total'] = subtotal_rounded

        # Write with safe context to avoid recursion
        return super(AccountMoveLine, self.with_context(skip_custom_write=True)).write(new_vals)

    @api.depends('price_unit', 'quantity', 'discount_fixed', 'currency_id')
    def _compute_price_subtotal(self):
        for line in self:
            currency = line.currency_id or line.company_id.currency_id

            base = line.price_unit * line.quantity
            clean_subtotal = max(base - line.discount_fixed, 0.0)
            clean_subtotal_rounded = float_round(clean_subtotal, precision_rounding=currency.rounding)

            line.price_subtotal = clean_subtotal_rounded
            line.price_total = clean_subtotal_rounded
