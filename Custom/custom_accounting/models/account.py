from odoo import models, fields


class Account(models.Model):
	_name = "custom.account"
	_description = "Basic Account"

	name = fields.Char("Account Name", required=True)
	debit_entries = fields.One2many("custom.entry", "debit_account", string="Debit Entries")
	credit_entries = fields.One2many("custom.entry", "credit_account", string="Credit Entries")
	currency = fields.Many2one("res.currency", string="Account Currency", required=True)
	balance = fields.Monetary("Balance", currency_field="currency", compute='calculate_balance')
	parent_account = fields.Many2one("custom.account", string="Parent Account")
	child_accounts = fields.One2many("custom.account", inverse_name='parent_account', string="Child Accounts")
	account_type = fields.Selection(string="Account Type", selection=[("expense", "Expense"),
																	  ("invest", "Investment"),
																	  ("bank", "Bank"),
																	  ("cod", "Cash-on-Hand"),
																	  ("salary", "Salary"),
																	  ("loan", "Loan")])

	def calculate_balance(self):
		for rec in self:
			rec.balance = 100
