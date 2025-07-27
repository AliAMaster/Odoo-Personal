from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Account(models.Model):
    _name = "custom.account"
    _description = "Basic Account"

    name = fields.Char("Account Name", required=True)
    debit_entries = fields.One2many("custom.entry", "debit_account", string="Debit Entries")
    credit_entries = fields.One2many("custom.entry", "credit_account", string="Credit Entries")
    currency = fields.Many2one("res.currency", string="Account Currency")
    balance = fields.One2many(comodel_name="custom.account_balance", inverse_name="account", string="Balance")
    parent_account = fields.Many2one(
        "custom.account",
        string="Parent Account",
        domain="[('id', '!=', id), ('id', 'not in', child_ids)]"
    )
    child_accounts = fields.One2many("custom.account", inverse_name='parent_account', string="Child Accounts")
    account_type = fields.Selection(string="Account Type", selection=[("expense", "Expense"),
                                                                      ("bank", "Bank"),
                                                                      ('asset', 'Asset'),
                                                                      ('income', 'Income')])

    def rebuild_balances(self):
        for rec in self:
            rec.balance.unlink()
            currency_map = {}

            # Add own debit entries
            for entry in rec.debit_entries:
                cur = entry.currency.id
                currency_map[cur] = currency_map.get(cur, 0) + entry.amount

            # Subtract own credit entries
            for entry in rec.credit_entries:
                cur = entry.currency.id
                currency_map[cur] = currency_map.get(cur, 0) - entry.amount

            # Aggregate one-level-down child balances
            for child in rec.child_accounts:
                child.rebuild_balances()
                for b in child.balance:
                    cur = b.currency.id
                    currency_map[cur] = currency_map.get(cur, 0) + b.amount

            rec.balance = [(0, 0, {'currency': cur, 'amount': amt}) for cur, amt in currency_map.items()]

    @api.onchange('parent_account')
    def _onchange_parent(self):
        for rec in self:
            if not rec.parent_account:
                continue
            if not rec.currency:
                rec.currency = rec.parent_account.currency
            elif rec.parent_account.currency and rec.currency != rec.parent_account.currency:
                raise ValidationError("Cannot change to parent account with different currency.")

            if rec.name:
                rec.name = rec.name[rec.name.rfind("\\") + 1:]
                rec.name = rec.parent_account.name + "\\" + rec.name

    @api.depends('child_accounts')
    def _compute_child_ids(self):
        for rec in self:
            rec.child_ids = rec._get_all_child_ids()

    def _get_all_child_ids(self):
        all_ids = set()
        children = self.child_accounts
        while children:
            next_children = self.env['custom.account'].browse()
            for child in children:
                if child.id not in all_ids:
                    all_ids.add(child.id)
                    next_children += child.child_accounts
            children = next_children
        return list(all_ids)

    child_ids = fields.Many2many("custom.account", compute="_compute_child_ids", string="All Descendants")

    @api.constrains('parent_account')
    def _check_parent_hierarchy(self):
        for rec in self:
            if rec.parent_account and rec.parent_account.id == rec.id:
                raise ValidationError("An account cannot be its own parent.")
            if rec.parent_account and rec.id in rec._get_all_child_ids():
                raise ValidationError("An account cannot be a descendant of its own child.")
