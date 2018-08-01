__author__ = "Michael PW"

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

TYPE = (
    ("tronton", _("Tronton")),
    ("diesel", _("Colt Diesel"))
)

class Truck(models.Model):
    _name = "dalsil.truck"
    _inherit = "ss.model"
    _description = "Truck"

    name = fields.Char("Nopol Truk", required=True)
    type_truck = fields.Selection(TYPE, "Tipe Truck", default=TYPE[0][0])
    note = fields.Text("Keterangan")
    active = fields.Boolean("Is Active ?", default=True)