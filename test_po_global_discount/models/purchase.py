from odoo import api, fields, models

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    
    general_discount = fields.Float(
        digits="Discount",
        string="Gen. Disc. (%)",
    )
    
    _sql_constrains = [
        (
            "general_discount_limit",
            "CHECK (general_discount <= 100.0)",
            "Discount must be lower than 100%",  
        ),
    ]
    
    @api.onchange("partner_id")
    def onchange_partner_id(self):
        res = super().onchange_partner_id()
        self.general_discount = (
            self.partner_id.commercial_partner_id.purchase_general_discount
        )
        return res
    
    @api.onchange("general_discount")
    def onchange_general_discount(self):
        discount_field = 'discount'
        self.mapped("order_line").update({discount_field: self.general_discount})
        
    def action_update_general_discount(self):
        for order in self:
            order.onchange_general_discount()
            
    @api.model
    def _get_view(self, view_id=None, view_type="form", **options):
        arch, view = super()._get_view(view_id=view_id, view_type=view_type, **options)
        
        if view_type == "form":
            order_line_fields  = arch.xpath("//field[@name='order_line']")
            if order_line_fields:
                order_line_field = order_line_fields[0]
                context = order_line_field.attrib.get("context", "{}").replace(
                    "{", "{'default_discount': general_discount, ",1,
                )
                order_line_field.attrib["context"] = context
        return arch, view