# Copyright (C) 2012-Today - KMEE (<http://kmee.com.br>).
#  @author Luis Felipe Miléo - mileo@kmee.com.br
#  @author Renato Lima - renato.lima@akretion.com.br
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.addons import decimal_precision as dp
from odoo.exceptions import ValidationError, UserError

from ..constants import (
    AVISO_FAVORECIDO,
    BOLETO_ESPECIE,
)


class AccountPaymentMode(models.Model):
    _name = 'account.payment.mode'
    _inherit = [
	'account.payment.mode',
	'l10n_br.cnab.configuration',
	'mail.thread',
    ]

    internal_sequence_id = fields.Many2one(
        comodel_name='ir.sequence',
        string='Sequência',
    )

    instructions = fields.Text(
        string='Instruções de cobrança',
    )

    invoice_print = fields.Boolean(
        string='Gerar relatorio na conclusão da fatura?'
    )

    condition_issuing_paper = fields.Selection(
        selection=[
            ('1', 'Banco emite e Processa'),
            ('2', 'Cliente emite e banco processa')],
        string='Condição Emissão de Papeleta',
        default='1',
    )

    communication_2 = fields.Char(
        string='Comunicação para o sacador avalista',
    )

    code_convetion = fields.Char(
        string='Código do Convênio no Banco',
        size=20,
        help='Campo G007 do CNAB',
        track_visibility='always',
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
        default=0,
    )

    # A exportação CNAB não se encaixa somente nos parâmetros de
    # débito e crédito.
    boleto_wallet = fields.Char(
        string='Carteira',
        size=3,
        track_visibility='always',
    )

    boleto_modality = fields.Char(
        string='Modalidade',
        size=2,
        track_visibility='always',
    )

    boleto_variation = fields.Char(
        string='Variação',
        size=2,
        track_visibility='always',
    )

    boleto_accept = fields.Selection(
        selection=[
            ('S', 'Sim'),
            ('N', 'Não')],
        string='Aceite',
        default='N',
        track_visibility='always',
    )

    boleto_species = fields.Selection(
        selection=BOLETO_ESPECIE,
        string='Espécie do Título',
        default='01',
        track_visibility='always',
    )

    # Na configuração ou implementação de outros campos é
    # melhor seguir a idéia abaixo pois os campos não são usados com
    # frequencia e incluir um campo do tipo Char permitindo que seja
    # informado o valor de acordo com a configuração do Boleto ao
    # invês de diversos campos do Tipo Select para cada Banco parece
    # ser melhor.
    # [ Deixado manualmente, pois cada banco parece ter sua tabela.
    # ('0', u'Sem instrução'),
    # ('1', u'Protestar (Dias Corridos)'),
    # ('2', u'Protestar (Dias Úteis)'),
    # ('3', u'Não protestar'),
    # ('7', u'Negativar (Dias Corridos)'),
    # ('8', u'Não Negativar')
    # ]
    boleto_protest_code = fields.Char(
        string='Código de Protesto',
        default='0',
        help='Código adotado pela FEBRABAN para identificar o tipo '
             'de prazo a ser considerado para o protesto.',
        track_visibility='always',
    )

    boleto_days_protest = fields.Char(
        string='Número de Dias para Protesto',
        size=2,
        help='Número de dias decorrentes após a data de vencimento '
             'para inicialização do processo de cobrança via protesto.',
        track_visibility='always',
    )

    generate_own_number = fields.Boolean(
        string='Gerar nosso número?',
        default=True,
        help='Dependendo da carteira, banco, etc. '
             'O nosso número pode ser gerado pelo banco.',
    )

    product_tax_id = fields.Many2one(
        comodel_name='product.product',
        string='Taxa Adicional',
        track_visibility='always',
    )

    product_tax_account_id = fields.Many2one(
        comodel_name='account.account',
        string='Conta de Taxa do Produto',
        help='Conta padrão para a Taxa do Produto',
        track_visibility='always',
    )

    cnab_sequence_id = fields.Many2one(
        comodel_name='ir.sequence',
        string='Sequencia do Arquivo CNAB',
        track_visibility='always',
    )

    boleto_byte_idt = fields.Char(
        string='Byte IDT',
        size=1,
        help='Byte de identificação do cedente do bloqueto '
             'utilizado para compor o nosso número, '
             'usado pelos bancos Sicred/Unicred e Sicoob.',
        track_visibility='always',
    )

    boleto_post = fields.Char(
        string='Posto da Cooperativa de Crédito',
        size=2,
        help='Código do Posto da Cooperativa de Crédito,'
             ' usado pelos bancos Sicred/Unicred e Sicoob.',
        track_visibility='always',
    )

    # Field used to make invisible banks specifics fields
    bank_code_bc = fields.Char(
        related='fixed_journal_id.bank_id.code_bc',
    )

    own_number_sequence_id = fields.Many2one(
        comodel_name='ir.sequence',
        string='Sequência do Nosso Número',
        help='Para usar essa Sequencia é preciso definir o campo Tipo do '
             'Nosso Número como Sequencial Único por Carteira no cadastro da '
             'empresa',
        track_visibility='always',
    )

    # Field used to make invisible own_number_sequence_id
    own_number_type = fields.Selection(
        related='fixed_journal_id.company_id.own_number_type',
    )

    boleto_interest_code = fields.Char(
        string='Código da Mora',
        size=1,
        help='Código adotado pela FEBRABAN para identificação '
             'do tipo de pagamento de mora de juros.',
        track_visibility='always',
    )

    boleto_interest_perc = fields.Float(
        string='Percentual de Juros de Mora',
        digits=dp.get_precision('Account'),
        track_visibility='always',
    )

    # TODO - criar outro campo para separar a Conta Contabil de Multa ?
    #  o valor vem somado ao Juros Mora no retorno do cnab 400 unicred,
    #  isso seria o padrão dos outros bancos ?
    interest_fee_account_id = fields.Many2one(
        comodel_name='account.account',
        string='Conta Contabil de Juros Mora e Multa',
        help='Conta padrão para Juros Mora',
        track_visibility='always',
    )

    boleto_fee_code = fields.Char(
        string='Código da Multa',
        size=1,
        help='Código adotado pela FEBRABAN para identificação '
             'do tipo de pagamento de multa.',
        track_visibility='always',
    )

    boleto_fee_perc = fields.Float(
        string='Percentual de Multa',
        digits=dp.get_precision('Account'),
        track_visibility='always',
    )

    boleto_discount_perc = fields.Float(
        string=u"Percentual de Desconto até a Data de Vencimento",
        digits=dp.get_precision('Account'),
        track_visibility='always',
    )

    discount_account_id = fields.Many2one(
        comodel_name='account.account',
        string='Conta Contabil de Desconto',
        help='Conta padrão para Desconto',
        track_visibility='always',
    )

    rebate_account_id = fields.Many2one(
        comodel_name='account.account',
        string='Conta Contabil de Abatimanto',
        help='Conta padrão para Abatimento',
        track_visibility='always',
    )

    tariff_charge_account_id = fields.Many2one(
        comodel_name='account.account',
        string='Conta Contabil Tarifa Bancaria',
        help='Conta padrão para a Tarifa Bancaria',
        track_visibility='always',
    )

    payment_mode_line_ids = fields.One2many(
        comodel_name='account.payment.mode.line',
        inverse_name='payment_mode_id',
        string='Payment Mode Lines',
    )

    cnab_liq_return_move_code_ids = fields.Many2many(
        comodel_name='l10n_br_cnab.return.move.code',
        relation='l10n_br_cnab_return_liquidity_move_code_rel',
        column1='cnab_liq_return_move_code_id',
        column2='payment_mode_id',
        string='CNAB Liquidity Return Move Code',
        track_visibility='always',
    )

    # Codigo de Remessa/Inclusão de Registro Detalhe Liberado
    cnab_sending_code_id = fields.Many2one(
        comodel_name='l10n_br_cnab.mov.instruction.code',
        string='Sending Movement Instruction Code',
        help='Sending Movement Instruction Code',
        track_visibility='always',
    )

    # Codigo para Título/Pagamento Direto ao Fornecedor -Baixar
    cnab_write_off_code_id = fields.Many2one(
        comodel_name='l10n_br_cnab.mov.instruction.code',
        string='Write Off Movement Instruction Code',
        help='Write Off Movement Instruction Code',
        track_visibility='always',
    )

    # Field used to make invisible banks specifics fields
    bank_id = fields.Many2one(
        related='fixed_journal_id.bank_id',
    )

    @api.constrains(
        'boleto_type',
        'boleto_wallet',
        'boleto_modality',
        'boleto_variation',
    )
    def boleto_restriction(self):
        if self.bank_code_bc == '341' and not self.boleto_wallet:
            raise ValidationError('Carteira no banco Itaú é obrigatória')
        if self.group_lines:
            raise ValidationError(
                _('The Payment mode can not be used for Boleto/CNAB with the group'
                  ' lines active. \n Please uncheck it to continue.')
            )
        if self.generate_move or self.post_move:
            raise ValidationError(
                _('The Payment mode can not be used for Boleto/CNAB with the'
                  ' generated moves or post moves active. \n Please uncheck it'
                  ' to continue.')
            )

    @api.onchange('product_tax_id')
    def _onchange_product_tax_id(self):
        if not self.product_tax_id:
            self.tax_account_id = False

    @api.multi
    def get_own_number_sequence(self, inv, numero_documento):
        if inv.company_id.own_number_type == '0':
            # SEQUENCIAL_EMPRESA
            sequence = inv.company_id.own_number_sequence_id.next_by_id()
        elif inv.company_id.own_number_type == '1':
            # SEQUENCIAL_FATURA
            sequence = numero_documento.replace('/', '')
        elif inv.company_id.own_number_type == '2':
            # SEQUENCIAL_CARTEIRA
            sequence = inv.payment_mode_id.own_number_sequence_id.next_by_id()
        else:
            raise UserError(_(
                'Favor acessar aba Cobrança da configuração da'
                ' sua empresa para determinar o tipo de '
                'sequencia utilizada nas cobrancas'
            ))

        return sequence

    @api.constrains('boleto_discount_perc')
    def _check_discount_perc(self):
        for record in self:
            if record.boleto_discount_perc > 100 or\
               record.boleto_discount_perc < 0:
                raise ValidationError(
                    _('O percentual deve ser um valor entre 0 a 100.'))
