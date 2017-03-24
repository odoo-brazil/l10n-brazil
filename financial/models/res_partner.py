# -*- coding: utf-8 -*-
# Copyright 2017 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class ResPartner(models.Model):

    _inherit = 'res.partner'

    credit_limit = fields.Monetary(
        string=_('Limite de Crédito'),
    )
    available_credit_limit = fields.Monetary(
        string=_('Available Credit Limit'),
        compute='_compute_available_credit_limit',
    )
    credit = fields.Monetary()
    confirmed_orders = fields.Boolean()
    draft_invoices = fields.Boolean()

    @api.depends('credit_limit', 'credit')
    def _compute_available_credit_limit(self):
        config = self.env['account.config.settings'].search([
            ('company_id', '=', 1)])[-1]
        draft_inv = 0
        sale_ord = 0
        for record in self:
            record.available_credit_limit = record.credit_limit - record.credit
            print record.available_credit_limit
            if config.confirmed_orders:
                sale_env = self.env['sale.order'].search([(
                    'partner_id', '=', record.id)])
                for records in sale_env:
                    if (records.state == 'sale' and records.
                            invoice_status == 'to invoice'):
                        sale_ord += records.amount_total
                record.available_credit_limit -= sale_ord
            if config.draft_invoices:
                invoice_env = self.env['account.invoice'].search([(
                    'commercial_partner_id', '=', record.id)])
                for records in invoice_env:
                    if records.state == 'draft':
                        draft_inv += records.amount_total_signed
                record.available_credit_limit -= draft_inv
