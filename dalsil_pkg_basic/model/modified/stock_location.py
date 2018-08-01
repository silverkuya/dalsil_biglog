from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class StockLocation(models.Model):
    """
    Account Invoice
    """
    _inherit = "stock.location"

    group_location_id = fields.Many2one("dalsil.group_location")