# Copyright (C) 2016-Today - KMEE (<http://kmee.com.br>).
#  Luis Felipe Miléo - mileo@kmee.com.br
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp
from odoo.tools.float_utils import float_round as round

from ..constants import (
    AVISO_FAVORECIDO,
    CODIGO_FINALIDADE_TED,
    COMPLEMENTO_TIPO_SERVICO,
)


class AccountPaymentLine(models.Model):
    _name = 'account.payment.line'
    _inherit = ['account.payment.line', 'l10n_br.cnab.configuration']

    digitable_line = fields.Char(
        string='Linha Digitável',
    )

    percent_interest = fields.Float(
        string='Percentual de Juros',
        digits=dp.get_precision('Account'),
    )

    amount_interest = fields.Float(
        string='Valor Juros',
        compute='_compute_interest',
        digits=dp.get_precision('Account'),
    )

    own_number = fields.Char(
        string='Nosso Numero',
    )

    document_number = fields.Char(
        string='Número documento',
    )

    company_title_identification = fields.Char(
        string='Identificação Titulo Empresa',
    )

    doc_finality_code = fields.Selection(
        selection=COMPLEMENTO_TIPO_SERVICO,
        string='Complemento do Tipo de Serviço',
        help='Campo P005 do CNAB',
    )

    ted_finality_code = fields.Selection(
        selection=CODIGO_FINALIDADE_TED,
        string='Código Finalidade da TED',
        help='Campo P011 do CNAB',
    )

    complementary_finality_code = fields.Char(
        string='Código de finalidade complementar',
        size=2,
        help='Campo P013 do CNAB',
    )

    favored_warning = fields.Selection(
        selection=AVISO_FAVORECIDO,
        string='Aviso ao Favorecido',
        help='Campo P006 do CNAB',
        default='0',
    )

    rebate_value = fields.Float(
        string='Valor do Abatimento',
        help='Campo G045 do CNAB',
        default=0.00,
        digits=(13, 2),
    )

    discount_value = fields.Float(
        string='Valor do Desconto',
        digits=(13, 2),
        default=0.00,
        help='Campo G046 do CNAB',
    )

    interest_value = fields.Float(
        string='Valor da Mora',
        digits=(13, 2),
        default=0.00,
        help='Campo G047 do CNAB',
    )

    fee_value = fields.Float(
        string='Valor da Multa',
        digits=(13, 2),
        default=0.00,
        help='Campo G048 do CNAB',
    )

    payment_mode_id = fields.Many2one(
        comodel_name='account.payment.mode',
        string='Payment Mode',
        ondelete='set null',
    )

    payment_mode_line_id = fields.Many2one(
        comodel_name='account.payment.mode.line',
        string='Payment Mode Line',
        ondelete='set null',
        domain="[('payment_mode_id', '=', payment_mode_id)]"
    )

    @api.depends('payment_mode_id')
    def _compute_bank_id(self):
        for record in self:
            record.bank_id = record.payment_mode_id.fixed_journal_id.bank_id

    @api.onchange('payment_mode_line_id')
    def _onchange_payment_mode_line_id(self):
        self.service_type_id = self.payment_mode_line_id.service_type_id
        self.release_form_id = self.payment_mode_line_id.release_form_id
        self.doc_finality_code_id = \
            self.payment_mode_line_id.doc_finality_code_id
        self.ted_finality_code_id = \
            self.payment_mode_line_id.ted_finality_code_id

    @api.multi
    @api.depends('percent_interest', 'amount_currency')
    def _compute_interest(self):
        for record in self:
            precision = record.env[
                'decimal.precision'].precision_get('Account')
            record.amount_interest = round(
                record.amount_currency * (
                    record.percent_interest / 100), precision)

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        mode = (
            self.env['account.payment.order']
            .browse(self.env.context.get('order_id'))
            .payment_mode_id
        )
        if mode.doc_finality_code:
            res.update({'doc_finality_code': mode.doc_finality_code})
        if mode.ted_finality_code:
            res.update({'ted_finality_code': mode.ted_finality_code})
        if mode.complementary_finality_code:
            res.update(
                {'complementary_finality_code': mode.complementary_finality_code}
            )
        if mode.favored_warning:
            res.update({'favored_warning': mode.favored_warning})
        return res
