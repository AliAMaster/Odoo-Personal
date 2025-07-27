from odoo import models, fields, api


class WorkOut(models.Model):
    _name = "workout"
    _description = "Workout"

    sequence = fields.Char(string="#", readonly=True, copy=False, default="/")
    set = fields.One2many(comodel_name="set", inverse_name="workout")
    date_time = fields.Datetime("Time", default=lambda self: fields.datetime.now(), readonly=True)
    location = fields.Many2one(comodel_name="location")

    @api.model_create_multi
    def create(self, vals_list: list):
        for vals in vals_list:
            if not vals.get('sequence'):
                vals['sequence'] = self.env['ir.sequence'].next_by_code('workout.sequence')
        return super().create(vals_list)
