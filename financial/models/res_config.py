# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AccountConfigSettings(models.TransientModel):
    _inherit = 'account.config.settings'

    confirmed_orders = fields.Boolean()
    draft_invoices = fields.Boolean()
    sale_installed = fields.Boolean(
        compute='compute_is_sale_installed',
    )

    @api.depends('draft_invoices')
    def compute_is_sale_installed(self):
        ir_module = self.env['ir.module.module']
        res_found_module = ir_module.search_count([
            ('name', '=', 'sale'),
            ('state', '=', 'installed')])
        if res_found_module:
            for line in self:
                line.sale_installed = True

    @api.model
    def get_default_credit_control(self, fields):
        company = self.env.user.partner_id
        return {
            'confirmed_orders': company.confirmed_orders,
            'draft_invoices': company.draft_invoices,
        }

    @api.one
    def set_credit_control(self):
        company = self.env.user.partner_id
        company.confirmed_orders = self.confirmed_orders
        company.draft_invoices = self.draft_invoices
