from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Config(models.Model):
    """
    Model untuk config
    """
    _name = "dalsil.config"

    product_sangu_driver = fields.Many2one("product.product", "Product Sangu Driver")
    product_sangu_kuli = fields.Many2one("product.product", "Product Sangu Kuli")
    product_solar = fields.Many2one("product.product", "Product Solar")
    product_tol = fields.Many2one("product.product", "Product Tol")
    product_parkir = fields.Many2one("product.product", "Product Parkir")
    product_premi = fields.Many2one("product.product", "Product Premi")
    product_invoice = fields.Many2one("product.product", "Product Invoice")
    product_semen = fields.Many2one("product.product", "Product Semen")
    product_bata = fields.Many2one("product.product", "Product Bata")

    acc_sangu_driver = fields.Many2one("account.account", "Account Sangu Driver")
    acc_sangu_kuli = fields.Many2one("account.account", "Account Sangu Kuli")
    acc_solar = fields.Many2one("account.account", "Account Solar")
    acc_tol = fields.Many2one("account.account", "Account Tol")
    acc_parkir = fields.Many2one("account.account", "Account Parkir")
    acc_premi = fields.Many2one("account.account", "Account Premi")
    acc_invoice = fields.Many2one("account.account", "Account Invoice")

    partner_sangu_kuli = fields.Many2one("res.partner", "Partner Sangu Kuli")
    partner_solar = fields.Many2one("res.partner", "Partner Solar")
    partner_tol = fields.Many2one("res.partner", "Partner Tol")
    partner_parkir = fields.Many2one("res.partner", "Partner Parkir")
    partner_premi = fields.Many2one("res.partner", "Partner Premi")
    
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