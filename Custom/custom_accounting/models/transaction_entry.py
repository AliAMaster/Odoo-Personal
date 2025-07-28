from odoo import models, fields, api
from odoo.api import model, ValuesType, Self
from odoo.exceptions import ValidationError


class TransactionEntry(models.Model):
	_name = "custom.entry"
	_description = "Basic Transaction"
	_order = "sequence"

	sequence = fields.Char(string='#', readonly=True, copy=False)
	currency = fields.Many2one("res.currency", string="Currency")
	amount = fields.Monetary("Amount", currency_field="currency", required=True)
	transaction_date = fields.Date("Date", required=True)
	remark = fields.Char("Remarks")
	debit_account = fields.Many2one(
		"custom.account",
		string="Debit Account",
		required=True,
		domain="[('currency', '=', currency)]"
	)
	credit_account = fields.Many2one(
		"custom.account",
		string="Credit Account",
		required=True,
		domain="[('currency', '=', currency)]"
	)

	@api.model_create_multi
	def create(self, vals_list: list):
		for vals in vals_list:
			if not vals.get('sequence'):
				vals['sequence'] = self.env['ir.sequence'].next_by_code('custom.entry.seq')
		return super().create(vals_list)

	@api.onchange('debit_account', 'credit_account')
	def _onchange_accounts_set_currency(self):
		for rec in self:
			if not rec.currency:
				rec.currency = rec.debit_account.currency or rec.credit_account.currency

	@api.constrains('debit_account', 'credit_account')
	def _check_account_currency(self):
		for rec in self:
			if not rec.debit_account.currency:
				raise ValidationError("Debit account must have a currency.")
			if not rec.credit_account.currency:
				raise ValidationError("Credit account must have a currency.")
