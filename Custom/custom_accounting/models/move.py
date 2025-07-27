from odoo import models, fields

class AccountMove(models.Model):
	_name = "custom.move"
	_description = "Planned Transaction"
	_order = "sequence"

	sequence = fields.Char(string='#', readonly=True, copy=False, default='/')