# -*- coding: utf-8 -*-
# Copyright 2020 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class AccountPaymentModeLine(models.Model):

    _name = 'account.payment.mode.line'
    _inherit = 'l10n_br.cnab.configuration'

    name = fields.Char(
        string='Name',
    )

    payment_mode_id = fields.Many2one(
        comodel_name='account.payment.mode',
        string='Payment Mode',
        ondelete='cascade',
    )

    @api.depends('payment_mode_id')
    def _compute_bank_id(self):
        for record in self:
            record.bank_id = record.payment_mode_id.fixed_journal_id.bank_id
