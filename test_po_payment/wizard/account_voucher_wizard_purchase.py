from odoo import api, exceptions, fields, models
from odoo.tools.translate import _ # type: ignore

class AccountVoucherWizardPurchase(models.TransientModel):
    _name = "account.voucher.wizard.purchase"
    _description = "Account Voucher Wizard Purchase"

    order_id = fields.Many2one("purchase.order", required=True)

    journal_id = fields.Many2one(
        "account.journal", "Journal", required=True, domain=[("type", "in", ("bank", "cash"))]
    )

    journal_currency_id = fields.Many2one(
        "res.currency", "Journal Currency", store=True, readonly=False, compute="_compute_get_journal_currency"
    )

    currency_id = fields.Many2one("res.currency", "Currency", readonly=True)

    amount_total = fields.Monetary(readonly=True)

    amount_advance = fields.Monetary(
        "Advance Amount", required=True, currency_field="journal_currency_id"
    )

    date = fields.Date(required=True, default=fields.Date.context_today)

    currency_amount = fields.Monetary(
        "Currency Amount", readonly=True, currency_field="currency_id", compute="_compute_currency_amount", store=True
    )

    payment_ref = fields.Char("Ref. ")

    payment_method_line_id = fields.Many2one(
        comodel_name="account.payment.method.line",
        string="Payment Method",
        readonly=False,
        store=True,
        compute="_compute_payment_method_line_id",
        domain="[('id', 'in', available_payment_method_line_ids)]",
    )

    available_payment_method_line_ids = fields.Many2many(
        comodel_name="account.payment.method.line",
        compute="_compute_available_payment_method_line_ids",
    )

    @api.depends("journal_id")
    def _compute_get_journal_currency(self):
        for wzd in self:
            wzd.journal_currency_id = (
                wzd.journal_id.currency_id.id
                or self.env.user.company_id.currency_id.id
            )

    @api.depends("journal_id")
    def _compute_payment_method_line_id(self):
        for wizard in self:
            if wizard.journal_id:
                available_payment_method_lines = (
                    wizard.journal_id._get_available_payment_method_lines("outbound")
                )
            else:
                available_payment_method_lines = False

            if available_payment_method_lines:
                # wizard.payment_method_line_id = available_payment_method_lines[0].origin
                wizard.payment_method_line_id = available_payment_method_lines[0]
            else:
                wizard.payment_method_line_id = False

    @api.depends("journal_id")
    def _compute_available_payment_method_line_ids(self):
        for wizard in self:
            if wizard.journal_id:
                wizard.available_payment_method_line_ids = (
                    wizard.journal_id._get_available_payment_method_lines("outbound")
                )
            else:
                wizard.available_payment_method_line_ids = False

    @api.constrains("amount_advance")
    def check_amount(self):
        for record in self:
            if record.journal_currency_id.compare_amounts(record.amount_advance, 0.0) <= 0:
                raise exceptions.ValidationError(_("Amount of Advance must be positive."))

            if record.env.context.get("active_id", False):
                if (
                    record.currency_id.compare_amounts(
                        record.currency_amount, record.order_id.amount_residual
                    ) > 0
                ):
                    raise exceptions.ValidationError(_("Amount of advance is greater than residual amount on purchase."))

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        purchase_ids = self.env.context.get("active_ids", [])
        if not purchase_ids:
            return res

        purchase_id = purchase_ids[0]
        purchase = self.env["purchase.order"].browse(purchase_id)

        if "amount_total" in fields_list:
            res.update(
                {
                    "order_id": purchase.id,
                    "amount_total": purchase.amount_residual,
                    "currency_id": purchase.currency_id.id,
                }
            )

        res["journal_id"] = (
            self.env["account.journal"].search(
                [
                    ("type", "in", ("bank", "cash")),
                    ("company_id", "=", purchase.company_id.id),
                    ("outbound_payment_method_line_ids", "!=", False),
                ],
                limit=1,
            ).id
        )

        return res

    @api.depends("journal_id", "date", "amount_advance", "journal_currency_id")
    def _compute_currency_amount(self):
        for record in self:
            if record.journal_currency_id != record.currency_id:
                record.currency_amount = record.journal_currency_id._convert(
                    record.amount_advance,
                    record.currency_id,
                    record.order_id.company_id,
                    record.date or fields.Date.today(),
                )
            else:
                record.currency_amount = record.amount_advance

    def make_advance_payment(self):
        # self.ensure_one()
        # payment_obj = self.env["account.payment"]
        # purchase_obj = self.env["purchase.order"]

        # purchase_ids = self.env.context.get("active_ids", [])
        # if purchase_ids:
        #     purchase_id = purchase_ids[0]
        #     purchase = purchase_obj.browse(purchase_id)
        #     payment_vals = self._prepare_payment_vals(purchase)
        #     payment = payment_obj.create(payment_vals)
        self.ensure_one()
        payment_obj = self.env["account.payment"]
        purchase_obj = self.env["purchase.order"]

        purchase_ids = self.env.context.get("active_ids", [])
        if purchase_ids:
            purchase_id = purchase_ids[0]
            purchase = purchase_obj.browse(purchase_id)
            payment_vals = self._prepare_payment_vals(purchase)
            payment = payment_obj.create(payment_vals)

            # === Tambahan untuk auto post ===
            param_auto_post = self.env["ir.config_parameter"].sudo().get_param("auto_post_advance_payments", "False")
            auto_post = param_auto_post.lower() == "true"
            if auto_post:
                payment.action_post()

            # Optional: kirim pesan log ke PO
            purchase.message_post(body=_(
                "Advance Payment of %s has been created%s."
            ) % (
                self.amount_advance,
                " and auto-posted" if auto_post else ""
            ))

        return {"type": "ir.actions.act_window_close"}

    def _prepare_payment_vals(self, purchase):
        partner_id = purchase.partner_id.commercial_partner_id.id
        return {
            "purchase_id": purchase.id,
            "date": self.date,
            "amount": self.amount_advance,
            "payment_type": "outbound",
            "partner_type": "supplier",
            "ref": self.payment_ref or purchase.name,
            "journal_id": self.journal_id.id,
            "currency_id": self.journal_currency_id.id,
            "partner_id": partner_id,
            "payment_method_line_id": self.payment_method_line_id.id,
        }
