from odoo import models, fields, api


class FixedDeposit(models.Model):
    _name = "fixed_deposit"
    _description = "Fixed Deposit"

    reference = fields.Char(string="Reference")
    start_date = fields.Date(string="Start Date", required=True, default=lambda self: fields.date.today())
    end_date = fields.Date(string="End Date", required=True)
    currency = fields.Many2one(comodel_name="res.currency", string="Currency")
    start_amount = fields.Monetary(string="Start Amount", currency_field='currency', required=True)
    duration = fields.Integer(string='')
    return_amount = fields.Monetary(string="Return Amount", currency_field='currency', required=True)
    annual_percentage = fields.Float(string="% p.a")
    credit_account = fields.Many2one(comodel_name="custom.account", string="From", required=True, domain="[('currecny', '=', currency)]")
    interim_account = fields.Many2one(comodel_name="custom.account", string="FD Account", required=True, domain="[('currency', '=', currency)]")
    debit_account = fields.Many2one(comodel_name="custom.account", string="To", required=True, domain="[('currecny', '=', currency)]")
    start_entry = fields.Many2one(comodel_name="custom.entry", string="Start Entry")
    end_entry = fields.Many2one(comodel_name="custom.entry", string="End Entry")

    @api.onchange('credit_account', 'debit_account', 'interim_account')
    def _onchange_accounts_set_currency(self):
        for rec in self:
            if not rec.currency:
                rec.currency = rec.debit_account.currency or rec.credit_account.currency or rec.interim_account.currency

    @api.onchange('credit_account', 'debit_account')
    def _onchange_c_d_account_set(self):
        for rec in self:
            if not rec.credit_account:
                rec.credit_account = rec.debit_account
            if not rec.debit_account:
                rec.debit_account = rec.credit_account

    @api.onchange('return_amount', 'start_date', 'end_date')
    def _onchange_return(self):
        for rec in self:
            if rec.start_date and rec.end_date:


