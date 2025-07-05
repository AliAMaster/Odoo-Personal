from odoo import models, fields

class ExpectedTransaction(models.Model):
    _name = "custom.exp_trans"
    _description = "Expected Transaction"

    currency = fields.Many2one("res.currency", string="Currency", required=True)
    amount = fields.Monetary("Amount", currency_field="currency", required=True)
    due_date = fields.Date("Date")