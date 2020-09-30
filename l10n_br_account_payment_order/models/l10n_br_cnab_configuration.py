# Copyright 2020 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class L10nBrCnabConfiguration(models.Model):
    _name = 'l10n_br.cnab.configuration'

    bank_id = fields.Many2one(
        comodel_name='res.bank',
        compute='_compute_bank_id',
    )

    service_type_id = fields.Many2one(
        comodel_name='l10n_br.cnab.option',
        string='Tipo de Serviço',
        help='Campo G025 do CNAB',
        domain='[("option_type", "=", "service_type"), '
               '("bank_id", "=", bank_id)]',
        store=True,
    )

    release_form_id = fields.Many2one(
        comodel_name='l10n_br.cnab.option',
        string='Forma Lançamento',
        help='Campo G029 do CNAB',
        domain='[("option_type", "=", "release_form"), '
               '("bank_id", "=", bank_id)]',
        store=True,
    )

    doc_finality_code_id = fields.Many2one(
        comodel_name='l10n_br.cnab.option',
        string='Complemento do Tipo de Serviço',
        help='Campo P005 do CNAB',
        domain='[("option_type", "=", "doc_finality_code"), '
               '("bank_id", "=", bank_id)]',
        store=True,
    )

    ted_finality_code_id = fields.Many2one(
        comodel_name='l10n_br.cnab.option',
        string='Código Finalidade da TED',
        help='Campo P011 do CNAB',
        domain='[("option_type", "=", "ted_finality_code"), '
               '("bank_id", "=", bank_id)]',
        store=True,
    )

    def _compute_bank_id(self):
        raise NotImplementedError
