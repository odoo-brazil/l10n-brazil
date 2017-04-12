# -*- coding: utf-8 -*-
# Copyright 2017 KMEE - Hendrix Costa <hendrix.costa@kmee.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64

from openerp import api, fields, exceptions, models, _

from l10n_br_hr_grrf import Grrf


class HrPayslip(models.Model):

    _inherit = 'hr.payslip'

    attachment_ids = fields.Many2many(
        comodel_name='ir.attachment',
        relation='hr_payslip_attachment_rel',
        column1='hr_payslip',
        column2='attachment_id',
        string=u'Attachments'
    )

    grrf = fields.Text(
        string='GRRF',
    )

    @api.multi
    def compute_grrf(self):
        """
        Método que inicia o processo para gerar novo GRRF. Disparado na view.
        :return:
        """
        for holerite in self:
            grrf = Grrf()
            self._compute_grrf(holerite, grrf)
            holerite.grrf = grrf._gerar_grrf()
            path_arquivo = grrf._gerar_arquivo_temp(holerite.grrf, 'GRRF')
            self._gerar_anexo('grrf.re', path_arquivo)

    def _compute_grrf(self, holerite, grrf):
        """
        Dado um holerite de rescisao preencher os campos do objeto de GRRF
        :param holerite:
        :param grrf:
        :return:
        """
        # Informações do Responsavel

        # Data de pagamento do holerite de rescisao
        grrf.data_recolhimento_grrf = ''
        # Pessoa que esta logada
        grrf.nome_do_contato_responsavel = self.env.user.name
        # Telefone pessoa que esta logada
        grrf.telefone_contato_responsavel = self.env.user.phone
        # Email do usuario logado
        grrf.email_contato = self.env.user.email

        # informações da Empresa
        grrf.tipo_de_inscricao_empresa = 1  # 1 (CNPJ) ou 2 (CEI)
        grrf.inscricao_da_empresa = self.company_id.cnpj_cpf
        grrf.razao_social_empresa = self.company_id.legal_name
        grrf.endereco_empresa = \
            self.company_id.street or '' + self.company_id.number or ''
        grrf.bairro_empresa = self.company_id.street2
        grrf.cep_empresa = self.company_id.zip
        grrf.cidade_empresa = self.company_id.l10n_br_city_id.name
        grrf.unidade_federacao_empresa = self.company_id.state_id.code
        grrf.telefone_empresa = self.company_id.phone
        grrf.CNAE_fiscal = self.company_id.cnae_main_id.code or ''
        grrf.fpas = u'515'              # Fixo

        if self.company_id.fiscal_type == 1:          # Simples nacional Odoo
            simples = 2                               # Simples do Layout
        else:                                         # Se nao for do simples
            simples = 1                               # 1 == Não Optante
        grrf.simples = simples

        # Informação do trabalhador
        funcionario = holerite.contract_id.employee_id
        grrf.PIS_PASEP = funcionario.pis_pasep
        grrf.data_admissao = holerite.contract_id.date_start
        # 01 Empregado; | 02 Trabalhador Avulso | 03 Trabalhador não vinculadO
        grrf.categoria_trabalhador = u'01'
        grrf.nome_do_trabalhador = funcionario.name
        grrf.numero_ctps = funcionario.ctps
        grrf.serie_ctps = funcionario.ctps_series
        grrf.sexo = funcionario.gender
        grrf.grau_de_instrucao = funcionario.educational_attainment.code
        grrf.data_nascimento = funcionario.birthday
        grrf.qtd_horas_trabalhadas_semana = holerite.contract_id.weekly_hours
        grrf.CBO = holerite.contract_id.job_id.cbo_id.code
        # Data admissao
        grrf.data_opcao = holerite.contract_id.date_start
        # Código de movimentação da sefip
        grrf.codigo_da_movimentacao = holerite.struct_id.tipo_afastamento_sefip
        # Data cara sai da empresa
        grrf.data_movimentacao = holerite.date_to
        grrf.codigo_de_saque = holerite.struct_id.tipo_saque
        grrf.aviso_previo = u'2'
        grrf.data_inicio_aviso_previo = holerite.date_from
        grrf.reposicao_de_vaga = u'N'

        remuneracao_mes_rescisao = 0
        aviso_previo_indenizado = 0
        for line in holerite.line_ids:
            if line.code == 'BASE_FGTS':
                remuneracao_mes_rescisao = line.total
            if line.code == 'BRUTO_AVISO_PREVIO':
                aviso_previo_indenizado = line.total

        # Get Rubrica do BASE_FGTS
        grrf.remuneracao_mes_rescisao = remuneracao_mes_rescisao
        # Rubrica Bruto Aviso previo para somar todos dados de aviso previo
        grrf.aviso_previo_indenizado = aviso_previo_indenizado

        grrf.CPF = funcionario.cpf
        grrf.banco_conta_trabalhador = ''
        grrf.agencia_trabalhador = ''
        grrf.conta_trabalhador = ''
        # saldo do FGTS consulta manual na caixa
        grrf.saldo_para_fins_rescisorios = holerite.saldo_para_fins_rescisorios

    def _gerar_anexo(self, nome_do_arquivo, path_arquivo_temp):
        """
        Função para gerar anexo dentro do holerite, apartir de um arquivo
        temporário. Deve ser passado o path do arquivo temporário que se
        tornará anexo da payslip
        :param nome_do_arquivo:
        :param path_arquivo_temp:
        :return:
        """
        try:
            file_attc = open(path_arquivo_temp, 'r')
            attc = file_attc.read()
            attachment_obj = self.env['ir.attachment']
            attachment_data = {
                'name': nome_do_arquivo,
                'datas_fname': nome_do_arquivo,
                'datas': base64.b64encode(attc),
                'res_model': 'hr.payslip',
                'res_id': self.id,
            }
            attachment_obj.create(attachment_data)
            file_attc.close()

        except:
            raise exceptions.Warning(
                _('Impossível gerar Anexo do %s' % nome_do_arquivo))
