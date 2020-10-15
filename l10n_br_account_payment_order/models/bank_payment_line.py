# © 2012 KMEE INFORMATICA LTDA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models

from ..constants import (
    AVISO_FAVORECIDO,
    ESTADOS_CNAB,
)


class BankPaymentLine(models.Model):
    _name = 'bank.payment.line'
    _inherit = ['bank.payment.line', 'l10n_br.cnab.configuration']

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        mode = (
            self.env['account.payment.order'].browse(
                self.env.context.get('order_id')).payment_mode_id
        )
        if mode.doc_finality_code_id:
            res.update({'doc_finality_code_id': mode.doc_finality_code_id})
        if mode.ted_finality_code_id:
            res.update({'ted_finality_code_id': mode.ted_finality_code_id})
        if mode.complementary_finality_code:
            res.update(
                {'complementary_finality_code': mode.complementary_finality_code}
            )
        if mode.favored_warning:
            res.update({'favored_warning': mode.favored_warning})
        return res

    complementary_finality_code = fields.Char(
        string='Código de finalidade complementar',
        size=2,
        help='Campo P013 do CNAB',
    )

    favored_warning = fields.Selection(
        selection=AVISO_FAVORECIDO,
        string='Aviso ao Favorecido',
        default='0',
        help='Campo P006 do CNAB',
    )

    rebate_value = fields.Float(
        string='Valor do Abatimento',
        digits=(13, 2),
        default=0.00,
        help='Campo G045 do CNAB',
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

    # TODO - mover os cnab/lote/evento para o modulo de implentacao da KMEE,
    #  já que para importacao do arquivo CNAB de retorno a Akretion passou a
    #  usar o account_move_base_import, estou mantendo o código para permirtir
    #  a extração e assim preservar o histórico de commits
    # event_id = fields.One2many(
    #    string='Eventos CNAB',
    #    comodel_name='l10n_br.cnab.evento',
    #    inverse_name='bank_payment_line_id',
    #    readonly=True,
    # )

    own_number = fields.Char(
        string='Nosso Numero',
    )

    document_number = fields.Char(
        string='Número documento',
    )

    company_title_identification = fields.Char(
        string='Identificação Titulo Empresa',
    )

    is_export_error = fields.Boolean(
        string='Contem erro de exportação',
    )

    export_error_message = fields.Char(
        string='Mensagem de erro',
    )

    last_cnab_state = fields.Selection(
        selection=ESTADOS_CNAB,
        string='Último Estado do CNAB',
        help='Último Estado do CNAB antes da confirmação de '
             'pagamento nas Ordens de Pagamento',
    )

    payment_mode_id = fields.Many2one(
        comodel_name='account.payment.mode',
        string='Payment Mode',
        ondelete='set null',
        domain="[('id', 'in', payment_mode_ids)]",
    )

    payment_mode_ids = fields.Many2many(
        comodel_name='account.payment.mode',
        string="Payment Modes",
        readonly=True,
        related='order_id.payment_mode_ids',
        domain="[('is_cnab_lot', '=', True)]",
    )

    @api.depends('payment_mode_id')
    def _compute_bank_id(self):
        for record in self:
            record.bank_id = record.payment_mode_id.fixed_journal_id.bank_id
            record.service_type_id = record.payment_mode_id.service_type_id
            record.release_form_id = record.payment_mode_id.release_form_id
            record.doc_finality_code_id = \
                record.payment_mode_id.doc_finality_code_id
            record.ted_finality_code_id = \
                record.payment_mode_id.ted_finality_code_id

    @api.multi
    def unlink(self):
        for record in self:
            if not record.last_cnab_state:
                continue

            move_line_id = self.env['account.move.line'].search(
                [
                    (
                        'company_title_identification',
                        '=',
                        record.company_title_identification,
                    )
                ]
            )
            move_line_id.state_cnab = record.last_cnab_state

        return super().unlink()

    @api.model
    def same_fields_payment_line_and_bank_payment_line(self):
        """
        This list of fields is used both to compute the grouping
        hashcode and to copy the values from payment line
        to bank payment line
        The fields must have the same name on the 2 objects
        """
        same_fields = super().same_fields_payment_line_and_bank_payment_line()

        # TODO: Implementar campo brasileiros que permitem mesclar linhas

        same_fields = []  # Por segurança não vamos mesclar nada
        #     'currency', 'partner_id',
        #     'bank_id', 'date', 'state']

        return same_fields
