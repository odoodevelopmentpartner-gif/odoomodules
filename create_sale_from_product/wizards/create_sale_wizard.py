from odoo import api, fields, models
from odoo.exceptions import UserError


class CreateSaleWizard(models.TransientModel):
    _name = 'create.sale.wizard'
    _description = 'Wizard to Create Sale Order from Products'

    partner_id = fields.Many2one('res.partner', string="Customer", required=True,
                                 domain=[('customer_rank', '>', 0)])
    order_date = fields.Datetime(string="Order Date", default=fields.Datetime.now())
    line_ids = fields.One2many('create.sale.wizard.line', 'wizard_id', string="Order Lines")

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)

        products = self.env.context.get("active_ids", [])
        line_vals = []

        for prod in self.env['product.product'].browse(products):
            line_vals.append((0, 0, {
                'product_id': prod.id,
                'quantity': 1.0,
                'price_unit': prod.lst_price,
            }))

        res["line_ids"] = line_vals
        return res

    def create_sale_order(self):
        if not self.partner_id:
            raise UserError("Please select a customer.")

        sale_order = self.env['sale.order'].create({
            'partner_id': self.partner_id.id,
            'date_order': self.order_date,
        })

        for line in self.line_ids:
            self.env['sale.order.line'].create({
                'order_id': sale_order.id,
                'product_id': line.product_id.id,
                'product_uom_qty': line.quantity,
                'price_unit': line.price_unit,
            })

        return {
            'name': "Sale Order",
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'res_id': sale_order.id,
        }


class CreateSaleWizardLine(models.TransientModel):
    _name = 'create.sale.wizard.line'
    _description = 'Sale Order Product Lines Wizard'

    wizard_id = fields.Many2one('create.sale.wizard')
    product_id = fields.Many2one('product.product', string="Product", required=True)
    quantity = fields.Float(string="Quantity", default=1.0)
    price_unit = fields.Float(string="Unit Price")


    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.price_unit = self.product_id.lst_price
