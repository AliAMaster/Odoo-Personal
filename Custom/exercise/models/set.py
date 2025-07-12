from email.policy import default

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Set(models.Model):
    _name = "set"
    _description = "Exercise Set"

    exercise = fields.Many2one(comodel_name="exercise", required=True)
    weight = fields.Float("Weight", required=False)
    weight_uom = fields.Many2one(comodel_name="uom.uom", string="", domain="[('category_id.name', '=', 'Weight')]",
                                 default=lambda self: self.env.ref('uom.product_uom_kgm'))
    repetition = fields.Integer("Repetition", required=True)
    workout = fields.Many2one(comodel_name="workout")
    datetime = fields.Datetime(string="date_time", default=lambda self: fields.datetime.now(), readonly=True)

    @api.constrains
    def check_weight_is_empty(self):
        for rec in self:
            if rec.weight and not rec.weight_uom:
                raise ValidationError("Select weight Unit.")
