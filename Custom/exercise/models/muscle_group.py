from odoo import models, fields


class MuscleGroup(models.Model):
    _name = "muscle_group"
    _description = "Muscle Group"

    name = fields.Char("Name", required=True)