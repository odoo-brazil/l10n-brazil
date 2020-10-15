# © 2012 KMEE INFORMATICA LTDA
#   @author Fernando Marcato <fernando.marcato@kmee.com.br>
#   @author  Hendrix Costa <hendrix.costa@kmee.com.br>
# Copyright (C) 2020 - KMEE (<http://kmee.com.br>).
#  author Daniel Sadamo <daniel.sadamo@kmee.com.br>
# Copyright (C) 2020 - Akretion (<http://akretion.com.br>).
#  author Magno Costa <magno.costa@akretion.com.br>
#  author Renato Lima <renato.lima@akretion.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

from ..constants import (
    CODIGO_INSTRUCAO_MOVIMENTO,
    FORMA_LANCAMENTO,
    FORMA_LANCAMENTO_ITAU,
    INDICATIVO_FORMA_PAGAMENTO,
    TIPO_MOVIMENTO,
    TIPO_SERVICO,
)

_logger = logging.getLogger(__name__)


class AccountPaymentOrder(models.Model):
    _name = 'account.payment.order'
    _inherit = ['account.payment.order', 'l10n_br.cnab.configuration']

    file_number = fields.Integer(
        string='Número sequencial do arquivo',
    )

    cnab_file = fields.Binary(
        string='CNAB File',
        readonly=True,
    )

    cnab_filename = fields.Char(
        string='CNAB Filename',
    )

    service_type = fields.Selection(
        selection=TIPO_SERVICO,
        string='Tipo de Serviço',
        help='Campo G025 do CNAB',
        default='30',
    )

    release_form = fields.Selection(
        selection=FORMA_LANCAMENTO,
        string='Forma Lançamento',
        help='Campo G029 do CNAB',
    )

    release_form_itau = fields.Selection(
        selection=FORMA_LANCAMENTO_ITAU,
        string='Forma Lançamento Itaú',
        help='Campo G029 do CNAB',
    )

    code_convetion = fields.Char(
        string='Código do Convênio no Banco',
        size=20,
        help='Campo G007 do CNAB',
        default='0001222130126',
    )

    indicative_form_payment = fields.Selection(
        selection=INDICATIVO_FORMA_PAGAMENTO,
        string='Indicativo de Forma de Pagamento',
        help='Campo P014 do CNAB',
        default='01',
    )

    movement_type = fields.Selection(
        selection=TIPO_MOVIMENTO,
        string='Tipo de Movimento',
        help='Campo G060 do CNAB',
        default='0',
    )

    movement_instruction_code = fields.Selection(
        selection=CODIGO_INSTRUCAO_MOVIMENTO,
        string='Código da Instrução para Movimento',
        help='Campo G061 do CNAB',
        default='00',
    )

    bank_line_error_ids = fields.One2many(
        comodel_name='bank.payment.line',
        inverse_name='order_id',
        string='Bank Payment Error Lines',
        readonly=True,
        domain=[('is_export_error', '=', True)],
    )

    @api.model
    def _prepare_bank_payment_line(self, paylines):
        result = super()._prepare_bank_payment_line(paylines)
        result['own_number'] = paylines[0].own_number
        result['document_number'] = paylines[0].document_number
        result['company_title_identification'] =\
            paylines[0].company_title_identification
        result['last_cnab_state'] = paylines[0].move_line_id.cnab_state
        result['payment_mode_id'] = paylines[0].payment_mode_id.id
        result['payment_mode_line_id'] = paylines[0].payment_mode_line_id.id
        result['service_type_id'] = paylines[0].service_type_id.id
        result['release_form_id'] = paylines[0].release_form_id.id
        result['doc_finality_code_id'] = paylines[0].doc_finality_code_id.id
        result['ted_finality_code_id'] = paylines[0].ted_finality_code_id.id
        return result

    @api.multi
    def open2generated(self):
        result = super().open2generated()

        if self.bank_line_error_ids:
            self.message_post(
                'Erro ao gerar o arquivo, verifique a aba Linhas com problemas'
            )
            return False
        self.message_post('Arquivo gerado com sucesso')
        return result

    @api.depends('company_partner_bank_id')
    def _compute_bank_id(self):
        for record in self:
            record.bank_id = record.company_partner_bank_id.bank_id
