from odoo import models, fields
from odoo.api import model, ValuesType, Self


class TransactionEntry(models.Model):
    _name = "custom.entry"
    _description = "Basic Transaction"
    _order = "sequence"

    sequence = fields.Char(string='#', readonly=True, copy=False, default='/')
    currency = fields.Many2one("res.currency", string="Currency", required=True)
    amount = fields.Monetary("Amount", currency_field="currency", required=True)
    transaction_date = fields.Date("Date")
    remark = fields.Char("Remarks")
    debit_account = fields.Many2one("custom.account", string="Debit Account", required=True)
    credit_account = fields.Many2one("custom.account", string="Credit Account", required=True)

    @model
    def create(self, vals_list: list[ValuesType]) -> Self:
        result = super(TransactionEntry).create(vals_list)
        if result['sequence'] == "/":
            result['sequence'] = self.env['ir.sequence'].next_by_code('custom.entry.seq')
        return result
