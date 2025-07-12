from odoo import models, fields


class GymLocation(models.Model):
    _name = "location"
    _description = "Gym Location"

    name = fields.Char("Name", required=True)
