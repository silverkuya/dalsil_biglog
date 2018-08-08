__author__ = "Michael PW"

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class GroupLocation(models.Model):
    _name = "dalsil.group_location"
    _inherit = "ss.model"
    _description = "Group Location"

    name = fields.Char("Nama Grup Lokasi", required=True)
    note = fields.Text("Keterangan")
    active = fields.Boolean("Is Active ?", default=True)
    location_ids = fields.One2many("stock.location", "group_location_id", "Lokasi")
    price_ids = fields.One2many("dalsil.group_location_pricelist", "parent_id", "Pricelist")

class GroupLocationPriceList(models.Model):
    _name = "dalsil.group_location_pricelist"
    _inherit = "ss.model"
    _description = "Group Location Pricelist"

    parent_id = fields.Many2one("dalsil.group_location", "Parent")
    dest_group_id = fields.Many2one("dalsil.group_location", "Tujuan Group Lokasi")
    price = fields.Float("Harga", digits=(20,2))