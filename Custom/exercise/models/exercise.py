from odoo import models, fields


class Exercise(models.Model):
    _name = "exercise"
    _description = "Exercise Variation"

    name = fields.Char("Name", required=True)
    muscle_group = fields.Many2many("muscle_group", string="Muscle Groups")
