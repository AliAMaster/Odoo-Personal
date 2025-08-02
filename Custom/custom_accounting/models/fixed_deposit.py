from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from calendar import isleap
from datetime import date


def days_in_year(year: int):
    return 366 if isleap(year) else 365


def calc_dur(start_date: date, end_date: date):
    if end_date.year == start_date.year:
        return (end_date - start_date).days / days_in_year(start_date.year)
    current_year = start_date.year
    years = (date(current_year, 12, 31) - start_date).days / days_in_year(current_year)
    print(current_year)
    for current_year in range(start_date.year + 1, end_date.year):
        print(current_year)
        years += 1
    years += (end_date - date(end_date.year, 1, 1)).days / days_in_year(end_date.year)
    return years


class FixedDeposit(models.Model):
    _name = "fixed_deposit"
    _description = "Fixed Deposit"

    fd_ref = fields.Many2one(comodel_name="custom.account", string="Reference", required=True)
    credit_account = fields.Many2one(comodel_name="custom.account", string="From", required=True, domain="[('currecny', '=', currency)]")
    debit_account = fields.Many2one(comodel_name="custom.account", string="To", required=True, domain="[('currecny', '=', currency)]")

    start_date = fields.Date(string="Start Date", required=True, default=lambda self: fields.date.today())
    end_date = fields.Date(string="End Date", required=True)
    dur_days = fields.Integer(string="Days", default=0)
    dur_months = fields.Integer(string="Months", default=0)
    dur_years = fields.Integer(string="Years", default=0)
    dur_change = fields.Char(string="", invisible=True, store=False)

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

    @api.onchange('start_date')
    def _set_start_state(self):
        for rec in self:
            if rec.dur_change == 'end' or ((rec.dur_years == 0 and rec.dur_months == 0 and rec.dur_days == 0) and rec.end_date):
                delta = rec.end_date - rec.start_date
                rec.dur_years = delta.years
                rec.dur_months = delta.months
                rec.dur_days = delta.days
            else:
                rec.end_date = rec.start_date + relativedelta(years=rec.dur_years, months=rec.dur_months, days=rec.dur_days)
            rec.dur_change = 'start'

    @api.onchange('end_date')
    def _set_end_state(self):
        for rec in self:
            if rec.dur_change == 'start' or ((rec.dur_years == 0 and rec.dur_months == 0 and rec.dur_days == 0) and rec.start_date):
                delta = rec.end_date - rec.start_date
                rec.dur_years = delta.years
                rec.dur_months = delta.months
                rec.dur_days = delta.days
            else:
                rec.start_date = rec.end_date - relativedelta(years=rec.dur_years, months=rec.dur_months, days=rec.dur_days)
            rec.dur_change = 'end'

    @api.onchange('dur_days', 'dur_months', 'dur_years')
    def _set_dur_state(self):
        for rec in self:
            if rec.dur_change:
                if rec.dur_change == "start":
                    rec.end_date = rec.start_date + relativedelta(years=rec.dur_years, months=rec.dur_months, days=rec.dur_days)
                elif rec.dur_change == 'end':
                    rec.start_date = rec.end_date - relativedelta(years=rec.dur_years, months=rec.dur_months, days=rec.dur_days)

    @api.onchange('start_amount', 'return_amount', 'start_date', 'end_date')
    def _set_pa(self):
        for rec in self:
            if rec.start_date and rec.end_date:
                years = calc_dur(rec.start_date, rec.end_date)
