from odoo import models, fields
from odoo.api import model


class TransactionEntry(models.Model):
    _name = "custom.entry"
    _description = "Basic Transaction"
    _order = "sequence"

    sequence = fields.Char(string='#', readonly=True, copy=False, default='/')
    currency = fields.Many2one("res.currency", string="Currency")
    amount = fields.Monetary("Amount", currency_field="currency")
    date = fields.Date("Date")
    remark = fields.Char("Remarks")
    debit_account = fields.Many2one("custom.account", string="Debit Account")
    credit_account = fields.Many2one("custom.account", string="Credit Account")

    @model
    def create(self, vals):
        if vals.get('sequence_number', '/') == '/':
            vals['sequence_number'] = self.env['ir.sequence'].next_by_code('custom.account.type.seq') or '/'
        return super().create(vals)
