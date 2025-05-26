from odoo import api, models
from odoo.tools import float_round

class AccountTax(models.Model):
    _inherit = "account.tax"

    @api.model
    def _convert_to_tax_base_line_dict(
        self, base_line,
        partner=None, currency=None, product=None, taxes=None, price_unit=None, quantity=None,
        discount=None, account=None, analytic_distribution=None, price_subtotal=None,
        is_refund=False, rate=None,
        handle_price_include=True,
        extra_context=None,
    ):
        res = super()._convert_to_tax_base_line_dict(
            base_line,
            partner=partner,
            currency=currency,
            product=product,
            taxes=taxes,
            price_unit=price_unit,
            quantity=quantity,
            discount=discount,
            account=account,
            analytic_distribution=analytic_distribution,
            price_subtotal=price_subtotal,
            is_refund=is_refund,
            rate=rate,
            handle_price_include=handle_price_include,
            extra_context=extra_context,
        )

        if base_line and base_line.discount_fixed:
            currency = base_line.currency_id or base_line.company_id.currency_id
            base_amount = base_line.price_unit * base_line.quantity
            adjusted_base = max(base_amount - base_line.discount_fixed, 0.0)

            adjusted_base_rounded = float_round(adjusted_base, precision_rounding=currency.rounding)

            res["price_unit"] = float_round(
                adjusted_base_rounded / base_line.quantity if base_line.quantity else 0.0,
                precision_rounding=currency.rounding
            )
            res["discount"] = 0.0
            res["price_subtotal"] = adjusted_base_rounded

        return res
