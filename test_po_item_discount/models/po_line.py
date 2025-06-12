from odoo import api, fields, models

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    discount = fields.Float(string="Disc. (%)", digits="Discount")
    
    _sql_constraints = [
        (
            "discount_limit", "CHECK (discount <= 100.0)", "Discount must be lower than 100%.",
        )
    ]
    
    def write(self, vals):
        res = super().write(vals)
        if "discount" in vals or "price_unit" in vals:
            for line in self.filtered(lambda l: l.order_id == "purchase"):
                moves = line.move_ids.filtered(
                    lambda s: s.state not in ("cancel", "done") and s.product_id == line.product_id
                )
                moves.write({"price_unit" : line._get_discounted_price_unit()})
        return res
    
    def _get_discounted_price_unit(self):
        self.ensure_one()
        if self.discount:
            return self.price_unit * (1 - self.discount / 100)
        return self.price_unit
    
    @api.depends("discount")
    def _compute_amount(self):
        return super()._compute_amount()
    
    def _convert_to_tax_base_line_dict(self):
        vals = super()._convert_to_tax_base_line_dict()
        vals["price_unit"] = self._get_discounted_price_unit()
        return vals