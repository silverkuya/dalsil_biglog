from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, date, time, timedelta
import xlwt

try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

MONTH = (
    ("1", _("January")),
    ("2", _("February")),
    ("3", _("March")),
    ("4", _("April")),
    ("5", _("May")),
    ("6", _("June")),
    ("7", _("July")),
    ("8", _("August")),
    ("9", _("September")),
    ("10", _("October")),
    ("11", _("November")),
    ("12", _("December"))
)

DICT_MONTH = {
    "1": "January",
    "2": "February",
    "3": "March",
    "4": "April",
    "5": "May",
    "6": "June",
    "7": "July",
    "8": "August",
    "9": "September",
    "10": "October",
    "11": "November",
    "12": "December"
}

class ReportRitase(models.TransientModel):
    """
    Wizard model untuk membuat laporan stock
    """
    _name = "dalsil.wiz_report_ritase"
    # _inherit = "ss.wizard"
    _description = "Wizard Generate Report Stock"

    partner_id = fields.Many2one("res.partner", "Driver", domain="[('active', '=', True), ('is_driver', '=', True)]")
    start_date = fields.Date('Tanggal Mulai', default=fields.Date.today())
    end_date = fields.Date('Tanggal Akhir', default=fields.Date.today())

    #################### Button ####################
    def generate_excel(self):
        """
        Membuatkan journal untuk pembayran expense
        """
        self.ensure_one()
        style_header = xlwt.easyxf('font: height 240, bold on')
        style_bold = xlwt.easyxf('font: bold on; align: horz center; '
                                 'borders: left thin, top thin, bottom thin, right thin')
        style_table = xlwt.easyxf('borders: left thin, bottom thin, right thin')

        wb = xlwt.Workbook("UTF-8")
        ws = wb.add_sheet('Laporan Ritase')

        y = 0
        x = 0

        ws.col(x).width = 800
        ws.col(x+1).width = 4200
        ws.col(x+2).width = 4200

        ws.write(y, x, 'LAPORAN RITASE', style=style_header)
        y += 1
        ws.write(y, x, '{} - {}'.format(self.start_date, self.end_date), style=style_header)
        y += 1

        domain = [
            ("active", "=", True),
            ("is_driver", "=", True)
        ]
        if self.partner_id:
            domain.append(("id", "=", self.partner_id.id))
        driver_ids = self.env["res.partner"].sudo().search(domain, order="name ASC")

        grand_total = 0
        for driver_id in driver_ids:
            y += 2
            ws.write(y, x, 'Supir:', style=xlwt.easyxf('font: bold on'))
            ws.write(y, x+2, str(driver_id.name))
            y += 1
            ritase_ids = self.env["dalsil.ritase"].sudo().search([
                ("driver_id", "=", driver_id.id),
                # ("state", "=", "done"),
                ("dt_spj", ">=", "{} 00:00:00".format(self.start_date)),
                ("dt_spj", "<=", "{} 23:59:59".format(self.end_date)),
            ], order="dt_spj ASC")
            ws.write(y, x, "No.", style=style_bold)
            ws.write(y, x+1, "No Dokumen", style=style_bold)
            ws.write(y, x+2, "Tanggal SPJ", style=style_bold)
            ws.write(y, x+3, "Truk", style=style_bold)
            ws.write(y, x+4, "Tipe Truk", style=style_bold)
            ws.write(y, x+5, "Tempat Angkut", style=style_bold)
            ws.write(y, x+6, "Grup Lokasi Tempat Angkut", style=style_bold)
            ws.write(y, x+7, "Tujuan Angkut", style=style_bold)
            ws.write(y, x+8, "Grup Lokasi Tujuan Angkut", style=style_bold)
            ws.write(y, x+9, "Destination Type", style=style_bold)
            ws.write(y, x+10, "Pengeluaran Ritase", style=style_bold)
            ws.write(y, x+11, "Pendapatan Ritase", style=style_bold)
            ws.write(y, x+12, "Total Pendapatan", style=style_bold)
            y += 1
            no_urut = 1
            grand_total_driver = 0
            for ritase_id in ritase_ids:
                ws.write(y, x, no_urut, style=style_table)
                ws.write(y, x+1, ritase_id.name, style=style_table)
                ws.write(y, x+2, ritase_id.dt_spj, style=style_table)
                ws.write(y, x+3, ritase_id.truck_id.name, style=style_table)
                ws.write(y, x+4, ritase_id.type_truck, style=style_table)
                ws.write(y, x+5, ritase_id.source_loc_id.name, style=style_table)
                ws.write(y, x+6, ritase_id.source_group_loc_id.name, style=style_table)
                ws.write(y, x+7, ritase_id.dest_loc_id.name, style=style_table)
                ws.write(y, x+8, ritase_id.dest_group_loc_id.name, style=style_table)
                ws.write(y, x+9, ritase_id.dest_type, style=style_table)
                ws.write(y, x+10, ritase_id.sangu_driver + ritase_id.sangu_kuli + ritase_id.solar + ritase_id.tol + ritase_id.parkir, style=style_table)
                ws.write(y, x+11, ritase_id.price, style=style_table)
                ws.write(y, x+12, ritase_id.total, style=style_table)
                grand_total_driver += ritase_id.total
                no_urut += 1
                y += 1
            ws.write(y, x+11, "Total", style=style_table)
            ws.write(y, x+12, grand_total_driver, style=style_table)
            y += 1
            grand_total += grand_total_driver
        ws.write(y, x+11, "Total Semua Supir", style=style_table)
        ws.write(y, x+12, grand_total, style=style_table)

        fp = StringIO()
        wb.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()

        return self.env["ss.download"].download(
            "Laporan_Ritase_{}.xls".format(datetime.today().strftime("%d%m%Y_%H %M")),
            data
        )