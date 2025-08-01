from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class FixedDeposit(models.Model):
    _name = "fixed_deposit"
    _description = "Fixed Deposit"

    fd_ref = fields.Many2one(comodel_name="custom.account", string="Reference", required=True)
    credit_account = fields.Many2one(comodel_name="custom.account", string="From", required=True, domain="[('currecny', '=', currency)]")
    debit_account = fields.Many2one(comodel_name="custom.account", string="To", required=True, domain="[('currecny', '=', currency)]")

    start_date = fields.Date(string="Start Date", required=True, default=lambda self: fields.date.today())
    end_date = fields.Date(string="End Date", required=True)
    dur_days = fields.Integer(string="Days")
    dur_months = fields.Integer(string="Months")
    dur_years = fields.Integer(string="Years")

    currency = fields.Many2one(comodel_name="res.currency", string="Currency")
    start_amount = fields.Monetary(string="Start Amount", currency_field='currency', required=True)
    return_amount = fields.Monetary(string="Return Amount", currency_field='currency', required=True)
    annual_percentage = fields.Float(string="% p.a")

    start_entry = fields.Many2one(comodel_name="custom.entry", string="Start Entry")
    end_entry = fields.Many2one(comodel_name="custom.entry", string="End Entry")

    @api.onchange('credit_account', 'debit_account', 'interim_account')
    def _onchange_accounts_set_currency(self):
        for rec in self:
            if not rec.currency:
                rec.currency = rec.debit_account.currency or rec.credit_account.currency

    @api.onchange('credit_account', 'debit_account')
    def _onchange_c_d_account_set(self):
        for rec in self:
            if not rec.credit_account:
                rec.credit_account = rec.debit_account
                rec.fd_ref.parent_account = rec.debit_account
            if not rec.debit_account:
                rec.debit_account = rec.credit_account
                rec.fd_ref.parent_account = rec.credit_account

    @api.onchange('start_date', 'end_date')
    def _set_duration(self):
        for rec in self:
            if rec.start_date and rec.end_date:
                delta = relativedelta(rec.start_date, rec.end_date)
                rec.dur_days = delta.days
                rec.dur_months = delta.months
                rec.dur_years = delta.years

    @api.onchange('start_date', 'dur_days', 'dur_months', 'dur_years')
    def _set_end_date(self):
        for rec in self:
            if rec.start_date:
                days = rec.dur_days if rec.dur_days else 0
                months = rec.dur_months if rec.dur_months else 0
                years = rec.dur_years if rec.dur_years else 0
                rec.end_date = rec.start_date + relativedelta(years=years, months=months, days=days)

    @api.onchange('end_date', 'dur_days', 'dur_months', 'dur_years')
    def _set_start_date(self):
        for rec in self:
            if rec.end_date:
                days = rec.dur_days if rec.dur_days else 0
                months = rec.dur_months if rec.dur_months else 0
                years = rec.dur_years if rec.dur_years else 0
                rec.start_date = rec.end_date - relativedelta(years=years, months=months, days=days)
