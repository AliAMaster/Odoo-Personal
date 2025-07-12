from odoo import models, fields
from odoo.api import model, ValuesType, Self


class WorkOut(models.Model):
    _name = "workout"
    _description = "Workout"

    sequence = fields.Char(string="#", readonly=True, copy=False, default="/")
    set = fields.One2many(comodel_name="set", inverse_name="workout")
    date_time = fields.Datetime("Time", default=lambda: fields.datetime.now(), readonly=True)
    location = fields.Many2one(comodel_name="location")

    @model
    def create(self, vals_list: list[ValuesType]) -> Self:
        result = super(WorkOut).create(vals_list)
        if result['sequence'] == "/":
            result['sequence'] = self.env['ir.sequence'].next_by_code('workout.sequence')
        return result
