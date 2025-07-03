from odoo import models, fields


class TransactionEntry(models.Model):
    _name = "custom.entry"
    _description = "Basic Transaction"
    _order = "sequence"

    sequence = fields.Integer('sequence', default=10)
    currency = fields.Many2one("res.currency", string="Entry Currency")
    amount = fields.Monetary("Amount", currency_field="currency")
    date = fields.Date("Date")
    remark = fields.Char("Remarks")
    debit_account = fields.Many2one("custom.account", string="Debit Account")
    credit_account = fields.Many2one("custom.account", string="Credit Account")
