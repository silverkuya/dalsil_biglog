from odoo import models, fields, api
from odoo.exceptions import ValidationError


class WizConfig(models.TransientModel):
    """
    Model untuk setting Config
    """
    _name = "dalsil.wiz_config"
    _inherit = "res.config.settings"

    product_sangu_driver = fields.Many2one("product.product", "Product Sangu Driver")
    product_sangu_kuli = fields.Many2one("product.product", "Product Sangu Kuli")
    product_solar = fields.Many2one("product.product", "Product Solar")
    product_tol = fields.Many2one("product.product", "Product Tol")
    product_parkir = fields.Many2one("product.product", "Product Parkir")
    product_semen = fields.Many2one("product.product", "Product Semen")
    product_bata = fields.Many2one("product.product", "Product Bata")

    acc_sangu_driver = fields.Many2one("account.account", "Account Sangu Driver")
    acc_sangu_kuli = fields.Many2one("account.account", "Account Sangu Kuli")
    acc_solar = fields.Many2one("account.account", "Account Solar")
    acc_tol = fields.Many2one("account.account", "Account Tol")
    acc_parkir = fields.Many2one("account.account", "Account Parkir")
    acc_invoice = fields.Many2one("account.account", "Account Invoice")

    tronton_bata_ringan_multiply = fields.Float("Bata Ringan Sangu Dibagi : ")
    tronton_semen_gudang_price = fields.Float("Biaya Semen Gudang ke Toko per Sack : ")
    colt_semen_gudang_price = fields.Float("Biaya Semen Gudang ke Toko per Sack : ")
    colt_bata_pabrik_price = fields.Float("Biaya Bata Ringan Pabrik ke Toko per Rit : ")
    colt_bata_gudang_price = fields.Float("Biaya Bata Ringan Gudang ke Toko per Rit : ")

    purc_journal_id = fields.Many2one("account.journal", "Journal Pembelian")
    purc_acc_credit_id = fields.Many2one("account.account", "Account Credit Pembelian")
    purc_acc_debit_id = fields.Many2one("account.account", "Account Debit Pembelian")
    inv_journal_id = fields.Many2one("account.journal", "Journal Pemakaian")
    inv_acc_credit_id = fields.Many2one("account.account", "Account Credit Pemakaian")
    inv_acc_debit_tronton_id = fields.Many2one("account.account", "Account Debit Pemakaian Tronton")
    inv_acc_debit_colt_id = fields.Many2one("account.account", "Account Debit Pemakaian Colt Diesel")

    @api.multi
    def set_setting(self):
        config = self.env["ir.model.data"].xmlid_to_object("dalsil_pkg_basic.dalsil_config")
        config.write({
            "product_sangu_driver": self.product_sangu_driver.id,
            "product_sangu_kuli": self.product_sangu_kuli.id,
            "product_solar": self.product_solar.id,
            "product_tol": self.product_tol.id,
            "product_parkir": self.product_parkir.id,
            "product_semen": self.product_semen.id,
            "product_bata": self.product_bata.id,
            "acc_sangu_driver": self.acc_sangu_driver.id,
            "acc_sangu_kuli": self.acc_sangu_kuli.id,
            "acc_solar": self.acc_solar.id,
            "acc_tol": self.acc_tol.id,
            "acc_parkir": self.acc_parkir.id,
            "acc_invoice": self.acc_invoice.id,
            "tronton_bata_ringan_multiply": self.tronton_bata_ringan_multiply,
            "tronton_semen_gudang_price": self.tronton_semen_gudang_price,
            "colt_semen_gudang_price": self.colt_semen_gudang_price,
            "colt_bata_pabrik_price": self.colt_bata_pabrik_price,
            "colt_bata_gudang_price": self.colt_bata_gudang_price,
            "purc_journal_id": self.purc_journal_id.id,
            "purc_acc_credit_id": self.purc_acc_credit_id.id,
            "purc_acc_debit_id": self.purc_acc_debit_id.id,
            "inv_journal_id": self.inv_journal_id.id,
            "inv_acc_credit_id": self.inv_acc_credit_id.id,
            "inv_acc_debit_tronton_id": self.inv_acc_debit_tronton_id.id,
            "inv_acc_debit_colt_id": self.inv_acc_debit_colt_id.id
        })

    @api.multi
    def get_default_setting(self, context):
        config = self.env["ir.model.data"].xmlid_to_object("dalsil_pkg_basic.dalsil_config")

        return {
            "product_sangu_driver": config.product_sangu_driver.id,
            "product_sangu_kuli": config.product_sangu_kuli.id,
            "product_solar": config.product_solar.id,
            "product_tol": config.product_tol.id,
            "product_parkir": config.product_parkir.id,
            "product_semen": config.product_semen.id,
            "product_bata": config.product_bata.id,
            "acc_sangu_driver": config.acc_sangu_driver.id,
            "acc_sangu_kuli": config.acc_sangu_kuli.id,
            "acc_solar": config.acc_solar.id,
            "acc_tol": config.acc_tol.id,
            "acc_parkir": config.acc_parkir.id,
            "acc_invoice": config.acc_invoice.id,
            "tronton_bata_ringan_multiply": config.tronton_bata_ringan_multiply,
            "tronton_semen_gudang_price": config.tronton_semen_gudang_price,
            "colt_semen_gudang_price": config.colt_semen_gudang_price,
            "colt_bata_pabrik_price": config.colt_bata_pabrik_price,
            "colt_bata_gudang_price": config.colt_bata_gudang_price,
            "purc_journal_id": config.purc_journal_id.id,
            "purc_acc_credit_id": config.purc_acc_credit_id.id,
            "purc_acc_debit_id": config.purc_acc_debit_id.id,
            "inv_journal_id": config.inv_journal_id.id,
            "inv_acc_credit_id": config.inv_acc_credit_id.id,
            "inv_acc_debit_tronton_id": config.inv_acc_debit_tronton_id.id,
            "inv_acc_debit_colt_id": config.inv_acc_debit_colt_id.id
        }
