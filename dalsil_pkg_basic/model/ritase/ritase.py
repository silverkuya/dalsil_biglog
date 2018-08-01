from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date, time, timedelta
import xlwt
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

STATE = (
    ("draft", _("Draft")),
    ("open", _("Open")),
    ("done", _("Done")),
    ("cancel", _("Cancelled")),
)

DEST_TYPE_TRONTON = (
    ("semen_pabrik", _("Semen Pabrik ke Toko")),
    ("semen_gudang", _("Semen Gudang ke Toko")),
    ("bata", _("Bata Ringan")),
    ("other", _("Barang Lainnya"))
)

DEST_TYPE_COLT_DIESEL = (
    ("semen_gudang", _("Semen Gudang ke Toko")),
    ("bata_pabrik", _("Bata Ringan Pabrik ke Toko")),
    ("bata_gudang", _("Bata Ringan Gudang ke Toko")),
    ("other", _("Barang Lainnya"))
)

DICT_DEST_TYPE_TRONTON = {
    "semen_pabrik": _("Semen Pabrik ke Toko"),
    "semen_gudang": _("Semen Gudang ke Toko"),
    "bata": _("Bata Ringan"),
    "other": _("Barang Lainnya")
}

DICT_DEST_TYPE_COLT_DIESEL = {
    "semen_gudang": _("Semen Gudang ke Toko"),
    "bata_pabrik": _("Bata Ringan Pabrik ke Toko"),
    "bata_gudang": _("Bata Ringan Gudang ke Toko"),
    "other": _("Barang Lainnya")
}

TYPE = (
    ("tronton", _("Tronton")),
    ("diesel", _("Colt Diesel"))
)


class Ritase(models.Model):
    """
    Rent Truck
    """
    _name = "dalsil.ritase"
    _inherit = "ss.model"
    _state_start = STATE[0][0]
    _seq_code = {"name": "dalsil_ritase"}

    name = fields.Char("Ritase No.")
    state = fields.Selection(STATE, "State", default="draft")
    truck_id = fields.Many2one("dalsil.truck", "Truck", domain=[
                               ("active", "=", True)], required=True)
    type_truck = fields.Selection(TYPE, "Tipe Truck", default=TYPE[0][
                                  0], compute="_get_truck_data", store=True)

    driver_id = fields.Many2one("res.partner", "Driver", domain=[(
        "active", "=", True), ("is_driver", "=", True)], required=True)
    kuli_id = fields.Many2one("res.partner", "Kuli", domain=[(
        "active", "=", True), ("is_kuli", "=", True)], required=True)
    solar_id = fields.Many2one("res.partner", "Solar", domain=[(
        "active", "=", True), ("is_solar", "=", True)], required=True)
    tol_id = fields.Many2one("res.partner", "Tol", domain=[(
        "active", "=", True), ("is_tol", "=", True)], required=True)
    parkir_id = fields.Many2one("res.partner", "Parkir", domain=[(
        "active", "=", True), ("is_parkir", "=", True)], required=True)
    # customer_rent_id = fields.Many2one("res.partner", "Penyewa Truck", domain=[("active", "=", True), ("customer", "=", True)], required=True)
    customer_id = fields.Many2one("res.partner", "Destination", domain=[(
        "active", "=", True), ("customer", "=", True)], required=True)
    source_loc_id = fields.Many2one("stock.location", "Tempat Angkut", domain=[
                                    ("active", "=", True)], required=True)
    source_group_loc_id = fields.Many2one(
        "dalsil.group_location", "Grup Lokasi Tempat Angkut", compute="_get_tempat_angkut_data")
    dest_loc_id = fields.Many2one("stock.location", "Tujuan Angkut", domain=[
                                  ("active", "=", True)], required=True)
    dest_group_loc_id = fields.Many2one(
        "dalsil.group_location", "Grup Lokasi Tujuan Angkut", compute="_get_tujuan_angkut_data")

    tronton_dest_type = fields.Selection(DEST_TYPE_TRONTON, "Destination Type")
    colt_dest_type = fields.Selection(
        DEST_TYPE_COLT_DIESEL, "Destination Type")
    dest_type = fields.Char(
        "Destination Type", compute="_get_destination_type", store=True)
    jumlah_barang = fields.Float("Jumlah Sak Semen")
    harga_persak = fields.Float("Harga Per Sak Semen")
    sangu_driver = fields.Float("Sangu Supir", digits=(20, 2))
    sangu_kuli = fields.Float("Sangu Kuli", digits=(20, 2))
    solar = fields.Float("Solar", digits=(20, 2))
    tol = fields.Float("Tol", digits=(20, 2))
    parkir = fields.Float("Parkir", digits=(20, 2))
    price = fields.Float("Harga Ritase", digits=(20, 2))
    total = fields.Float("Total Pendapatan", digits=(20,2))

    product_id = fields.Many2one("product.product", "Product")
    sangu_payment_term_id = fields.Many2one(
        'account.payment.term', string='Sangu Payment Terms')
    invoice_payment_term_id = fields.Many2one(
        'account.payment.term', string='Invoice Payment Terms')

    dt_spj = fields.Datetime("Tanggal SPJ")
    no_bukti = fields.Char("No Bukti")
    # dn_number = fields.Char("DN Number")
    # shipment_number = fields.Char("Shipment Number")

    # total_rent = fields.Integer("Total Amount", compute="_get_total_pay", store=True)
    note = fields.Text("Note")

    invoice_ids = fields.One2many("account.invoice", "ritase_id", "Invoice")
    # line_ids = fields.One2many("dalsil.rent_truck.line", "parent_id", "Product")
    # sangu_invoice_id = fields.Many2one("account.invoice", "Invoice Sangu", readonly="1")
    # rent_invoice_id = fields.Many2one("account.invoice", "Invoice Rent", readonly="1")
    # inv_invoice_id = fields.Many2one("account.invoice", "Customer Invoice", readonly="1")
    # pur_invoice_id = fields.Many2one("account.invoice", "Vendor Bill", readonly="1")

    @api.depends("truck_id", "tronton_dest_type", "colt_dest_type")
    def _get_destination_type(self):
        for record in self:
            if record.truck_id.type_truck == 'tronton':
                record.dest_type = DICT_DEST_TYPE_TRONTON[
                    record.tronton_dest_type]
            elif record.truck_id.type_truck == 'diesel':
                record.dest_type = DICT_DEST_TYPE_COLT_DIESEL[
                    record.colt_dest_type]

    @api.depends("truck_id")
    def _get_truck_data(self):
        for record in self:
            record.type_truck = record.truck_id.type_truck

    @api.depends("source_loc_id")
    def _get_tempat_angkut_data(self):
        for record in self:
            record.source_group_loc_id = record.source_loc_id.group_location_id

    @api.depends("dest_loc_id")
    def _get_tujuan_angkut_data(self):
        for record in self:
            record.dest_group_loc_id = record.dest_loc_id.group_location_id

    @api.multi
    def get_price(self):
        for record in self:
            setting = self.env["ir.model.data"].xmlid_to_object(
                "dalsil_pkg_basic.dalsil_config")
            if record.truck_id.type_truck == 'tronton':
                if record.tronton_dest_type == 'semen_pabrik':
                    pricelist = self.env["dalsil.group_location_pricelist"].sudo().search([
                        ("parent_id", "=", record.source_group_loc_id.id),
                        ("dest_group_id", "=", record.dest_group_loc_id.id)
                    ], order="create_date ASC", limit=1)
                    if not pricelist:
                        pricelist = self.env["dalsil.group_location_pricelist"].sudo().search([
                            ("dest_group_id", "=", record.source_group_loc_id.id),
                            ("parent_id", "=", record.dest_group_loc_id.id)
                        ], order="create_date ASC", limit=1)
                    if pricelist:
                        return pricelist.price
                elif record.tronton_dest_type == 'semen_gudang':
                    return record.jumlah_barang * record.harga_persak
                elif record.tronton_dest_type == 'bata':
                    return record.sangu_driver / setting.tronton_bata_ringan_multiply
            elif record.truck_id.type_truck == 'diesel':
                if record.colt_dest_type == 'semen_gudang':
                    return record.jumlah_barang * record.harga_persak
                elif record.colt_dest_type == 'bata_pabrik':
                    multiply = int(
                        (record.sangu_driver + record.sangu_kuli + record.solar + record.tol + record.parkir) / setting.colt_bata_pabrik_price) + 1
                    return multiply * setting.colt_bata_pabrik_price
                elif record.colt_dest_type == 'bata_gudang':
                    multiply = int(
                        (record.sangu_driver + record.sangu_kuli + record.solar + record.tol + record.parkir)/ setting.colt_bata_gudang_price) + 1
                    return multiply * setting.colt_bata_gudang_price
            return 0

    @api.onchange("type_truck", "source_group_loc_id", "dest_group_loc_id", "tronton_dest_type", "colt_dest_type", "jumlah_barang", "harga_persak", "sangu_driver", "sangu_kuli", "solar", "tol", "parkir")
    def onchange_price(self):
        self.price = self.get_price()
        self.total = self.price - (self.sangu_driver + self.sangu_kuli + self.solar + self.tol + self.parkir)

    @api.onchange("type_truck")
    def onchange_biaya(self):
        if self.type_truck != 'diesel':
            self.sangu_kuli = 0
            self.solar = 0
            self.tol = 0
            self.parkir = 0

    @api.onchange("tronton_dest_type", "colt_dest_type", "type_truck")
    def onchange_type(self):
        setting = self.env["ir.model.data"].xmlid_to_object(
                "dalsil_pkg_basic.dalsil_config")
        if self.type_truck == 'tronton':
            if self.tronton_dest_type in ['semen_pabrik', 'semen_gudang']:
                self.product_id = setting.product_semen
            elif self.tronton_dest_type in ['bata']:
                self.product_id = setting.product_bata
        elif self.type_truck == 'diesel':
            if self.colt_dest_type in ['semen_gudang']:
                self.product_id = setting.product_semen
            elif self.colt_dest_type in ['bata_pabrik', 'bata_gudang']:
                self.product_id = setting.product_bata

    @api.multi
    def to_open(self):
        for record in self:
            if record.price <= 0:
                raise ValidationError("Harga tidak boleh 0 atau minus")
            setting = self.env["ir.model.data"].xmlid_to_object(
                "dalsil_pkg_basic.dalsil_config")
            # setting = self.env['dalsil.wiz_config'].get_default_setting()
            vals = {
                'jenis_inv': "sangu_driver",
                'partner_id': record.driver_id.id,
                'origin': record.name,
                'type': 'in_invoice',
                'payment_term_id': record.sangu_payment_term_id.id,
                'ritase_id': record.id,
                'date_invoice': fields.Date.today(),
                'invoice_line_ids': [(0, 0, {
                    'product_id': setting.product_sangu_driver.id,
                    'name': 'Sangu Driver Ritase No ({})'.format(record.name),
                    'quantity': 1.0,
                    'price_unit': self.sangu_driver,
                    'account_id': setting.acc_sangu_driver.id
                })]
            }
            self.env['account.invoice'].sudo().create(vals)

            if record.sangu_kuli > 0:
                vals = {
                    'jenis_inv': "sangu_kuli",
                    'partner_id': record.kuli_id.id,
                    'origin': record.name,
                    'type': 'in_invoice',
                    'payment_term_id': record.sangu_payment_term_id.id,
                    'ritase_id': record.id,
                    'date_invoice': fields.Date.today(),
                    'invoice_line_ids': [(0, 0, {
                        'product_id': setting.product_sangu_kuli.id,
                        'name': 'Sangu Kuli Ritase No ({})'.format(record.name),
                        'quantity': 1.0,
                        'price_unit': self.sangu_kuli,
                        'account_id': setting.acc_sangu_kuli.id
                    })]
                }
                self.env['account.invoice'].sudo().create(vals)

            if record.solar > 0:
                vals = {
                    'jenis_inv': "solar",
                    'partner_id': record.solar_id.id,
                    'origin': record.name,
                    'type': 'in_invoice',
                    'payment_term_id': record.sangu_payment_term_id.id,
                    'ritase_id': record.id,
                    'date_invoice': fields.Date.today(),
                    'invoice_line_ids': [(0, 0, {
                        'product_id': setting.product_solar.id,
                        'name': 'Solar Ritase No ({})'.format(record.name),
                        'quantity': 1.0,
                        'price_unit': self.solar,
                        'account_id': setting.acc_solar.id
                    })]
                }
                self.env['account.invoice'].sudo().create(vals)

            if record.tol > 0:
                vals = {
                    'jenis_inv': "tol",
                    'partner_id': record.tol_id.id,
                    'origin': record.name,
                    'type': 'in_invoice',
                    'payment_term_id': record.sangu_payment_term_id.id,
                    'ritase_id': record.id,
                    'date_invoice': fields.Date.today(),
                    'invoice_line_ids': [(0, 0, {
                        'product_id': setting.product_tol.id,
                        'name': 'Solar Ritase No ({})'.format(record.name),
                        'quantity': 1.0,
                        'price_unit': self.tol,
                        'account_id': setting.acc_tol.id
                    })]
                }
                self.env['account.invoice'].sudo().create(vals)

            if record.parkir > 0:
                vals = {
                    'jenis_inv': "parkir",
                    'partner_id': record.parkir_id.id,
                    'origin': record.name,
                    'type': 'in_invoice',
                    'payment_term_id': record.sangu_payment_term_id.id,
                    'ritase_id': record.id,
                    'date_invoice': fields.Date.today(),
                    'invoice_line_ids': [(0, 0, {
                        'product_id': setting.product_parkir.id,
                        'name': 'Solar Ritase No ({})'.format(record.name),
                        'quantity': 1.0,
                        'price_unit': self.parkir,
                        'account_id': setting.acc_parkir.id
                    })]
                }
                self.env['account.invoice'].sudo().create(vals)

            vals = {
                'jenis_inv': "invoice",
                'partner_id': record.customer_id.id,
                'origin': record.name,
                'type': 'out_invoice',
                'payment_term_id': record.invoice_payment_term_id.id,
                'ritase_id': record.id,
                'date_invoice': fields.Date.today(),
                'invoice_line_ids': [(0, 0, {
                    'product_id': setting.product_invoice.id,
                    'name': 'Invoice Ritase No ({})'.format(record.name),
                    'quantity': 1.0,
                    'price_unit': self.price,
                    'account_id': setting.acc_invoice.id
                })]
            }
            self.env['account.invoice'].sudo().create(vals)
            record.state = 'open'

    @api.multi
    def to_done(self):
        for record in self:
            for invoice_id in record.invoice_ids:
                if invoice_id.state not in ['paid', 'cancel']:
                    raise ValidationError("Harap menyelesaikan invoice yang belum selesai terlebih dahulu")
            record.state = 'done'

    @api.multi
    def to_cancel(self):
        for record in self:
            for invoice_id in record.invoice_ids:
                if invoice_id.state != 'cancel':
                    raise ValidationError("Harap cancel semua invoice terlebih dahulu.")
            record.state = 'cancel'

    @api.multi
    def to_calculate(self):
        for record in self:
            invoice = 0
            sangu_driver = 0
            sangu_kuli = 0
            solar = 0
            tol = 0
            parkir = 0
            for invoice_id in record.invoice_ids:
                if invoice_id.jenis_inv == 'invoice':
                    invoice += invoice_id.amount_total
                elif invoice_id.jenis_inv == 'sangu_driver':
                    sangu_driver += invoice_id.amount_total
                elif invoice_id.jenis_inv == 'sangu_kuli':
                    sangu_kuli += invoice_id.amount_total
                elif invoice_id.jenis_inv == 'solar':
                    solar += invoice_id.amount_total
                elif invoice_id.jenis_inv == 'tol':
                    tol += invoice_id.amount_total
                elif invoice_id.jenis_inv == 'parkir':
                    parkir += invoice_id.amount_total
            record.sangu_driver = sangu_driver
            record.sangu_kuli = sangu_kuli
            record.solar = solar
            record.tol = tol
            record.parkir = parkir
            record.price = invoice
            record.total = self.price - (record.sangu_driver + record.sangu_kuli + record.solar + record.tol + record.parkir)

    @api.multi
    def to_print(self):
        self.ensure_one()
        style_default = xlwt.easyxf('font: height 240')
        style_header = xlwt.easyxf('font: height 280, bold on')
        style_bold = xlwt.easyxf('font: height 240, bold on; align: horz center; '
                                 'borders: left thin, top thin, bottom thin, right thin')
        style_table = xlwt.easyxf('font: height 240; borders: left thin, bottom thin, right thin')

        wb = xlwt.Workbook("UTF-8")
        ws = wb.add_sheet('SPJ')
        ws.footer_str = ''
        title = "SURAT PERINTAH JALAN"

        y = 0
        x = 0

        ws.col(x).width = 5000
        ws.col(x + 1).width = 12000
        ws.col(x + 2).width = 6000

        ws.row(0).height_mismatch = 1
        ws.row(0).height = 300
        ws.row(1).height_mismatch = 1
        ws.row(1).height = 280
        ws.row(2).height_mismatch = 1
        ws.row(2).height = 280
        ws.row(3).height_mismatch = 1
        ws.row(3).height = 280
        ws.row(4).height_mismatch = 1
        ws.row(4).height = 280
        ws.row(5).height_mismatch = 1
        ws.row(5).height = 280

        # ws.col(x + 3).width = 4500
        # ws.col(x + 4).width = 6000

        ws.write(y, x, "{} {}".format(title, self.name), style=style_header)
        y += 1
        ws.write(y, x, "Tanggal SPJ", style=style_default)
        ws.write(y, x + 1, self.dt_spj, style=style_default)
        y += 1
        ws.write(y, x, "Customer", style=style_default)
        ws.write(y, x + 1, self.customer_id.name, style=style_default)
        y += 1
        ws.write(y, x, "Tempat Angkut", style=style_default)
        ws.write(y, x + 1, "{} - {}".format(self.source_group_loc_id.name, self.source_loc_id.name), style=style_default)
        y += 1
        ws.write(y, x, "Tempat Bongkar", style=style_default)
        ws.write(y, x + 1, "{} - {}".format(self.dest_group_loc_id.name, self.dest_loc_id.name), style=style_default)
        y += 1
        ws.write(y, x, "No Bukti", style=style_default)
        ws.write(y, x + 1, self.no_bukti, style=style_default)
        y += 2

        ws.write(y, x, "No", style=style_bold)
        ws.write(y, x + 1, "Nama Barang", style=style_bold)
        ws.write(y, x + 2, "QTY", style=style_bold)
        y += 1

        # idx = 0
        # sum_qty = sum(self.invoice_line_ids.mapped("quantity"))
        # for inv_line_id in self.invoice_line_ids:
        #     ws.row(y).height_mismatch = 1
        #     ws.row(y).height = 280
        #     idx += 1
        #     tax_name = ""
        #     for tax_id in inv_line_id.invoice_line_tax_ids:
        #         tax_name += tax_id.name
        ws.write(y, x, 1, style=style_table)
        ws.write(y, x + 1, self.product_id.name, style=style_table)
        ws.write(y, x + 2, self.jumlah_barang, style=style_table)
        y += 1

        ws.write(y, x + 1, "Jml. Qty:", style=xlwt.easyxf('font: height 240; align: horiz right'))
        ws.write(y, x + 2, self.jumlah_barang, style=style_table)
        y += 3
        ws.write(y, x, "Adm. Penjualan,         Pengambil               Mengetahui, ", style=style_default)
        y += 3
        ws.write(y, x, "(____________)       (___________)         (___________)", style=style_default)

        fp = StringIO()
        wb.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()

        return self.env["ss.download"].download(
            "spj_{}.xls".format(self.name),
            data
        )