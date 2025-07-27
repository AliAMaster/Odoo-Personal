from odoo import models, fields, api


class Exercise(models.Model):
	_name = "exercise"
	_description = "Exercise Variation"

	name = fields.Char("Name", required=True)
	muscle_group = fields.Many2many("muscle_group", string="Muscle Groups")
	sets = fields.One2many(comodel_name="set", inverse_name='exercise', string="Sets", compute='compute_recent_sets')
	set_label = fields.Char(string="")

	@api.depends('sets.datetime')
	def compute_recent_sets(self):
		for rec in self:
			rec.sets = self.env['set'].search(
				[('exercise', '=', rec.id)],
				order='datetime desc',
				limit=3
			)
