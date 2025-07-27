from odoo import models, fields


class AccountBalance(models.Model):
    _name = "custom.account_balance"
    _description = "Account Balance"

    currency = fields.Many2one(comodel_name='res.currency', string='Currency')
    amount = fields.Monetary("Amount", currency_field="currency")
    account = fields.Many2one(comodel_name="custom.account", string="Account", ondelete="cascade")