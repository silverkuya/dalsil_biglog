from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, date, time, timedelta

STATE = (
    ("draft", _("Draft")),
    ("open", _("Open")),
    ("done", _("Done")),
    ("cancel", _("Cancelled")),
)

class Ritase(models.Model):
    """
    Rent Truck
    """
    _name = "dalsil.hutang_driver"
    _inherit = "ss.model"
    _state_start = STATE[0][0]
    _seq_code = {"name": "dalsil_hutang_driver"}

    name = fields.Char("Hutang Driver No.")
    state = fields.Selection(STATE, "State", default="draft")

    driver_id = fields.Many2one("res.partner", "Driver", domain=[(
        "active", "=", True), ("is_driver", "=", True)])
    ritase_id = fields.Many2one("dalsil.ritase", "Ritase", domain=[(
        "state", "in", ['open', 'done'])])
    hutang_driver = fields.Float("Hutang Supir", digits=(20, 2))
    payment_driver = fields.Float("Terbayar", digits=(20, 2))
    note = fields.Text("Note")

    @api.onchange("driver_id")
    def onchange_driver_id(self):
        ret = {'domain': {'driver_id': [("active", "=", True), ("is_driver", "=", True)]}}
        if self.driver_id:
            ret = {'domain': {'ritase_id': [('driver_id', '=', self.driver_id.id),("state", "in", ['open', 'done'])]}}
            if self.driver_id.id != self.ritase_id.driver_id.id:
                self.ritase_id = False 
        return ret

    @api.onchange("ritase_id")
    def onchange_ritase_id(self):
        if self.ritase_id:
            self.driver_id = self.ritase_id.driver_id.id

    @api.multi
    def to_done(self):
        for record in self:
            record.state = 'done'

    @api.multi
    def to_open(self):
        for record in self:
            record.state = 'open'

    @api.multi
    def to_cancel(self):
        for record in self:
            record.state = 'cancel'