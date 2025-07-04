from odoo import models, fields


class AccountType(models.Model):
    _name = "custom.account_type"
    _description = "Account Type"

    name = fields.Char(string="Name", required=True, placeholder="e.g. Salary")
