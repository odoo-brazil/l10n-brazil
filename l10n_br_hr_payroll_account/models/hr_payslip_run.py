# -*- coding: utf-8 -*-
# Copyright (C) 2016 KMEE (http://www.kmee.com.br)
# Copyright (C) 2018 ABGF (http://www.abgf.gov.br)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from __future__ import absolute_import, print_function, unicode_literals

from openerp import api, models, fields
from openerp.exceptions import Warning

NOME_LANCAMENTO_LOTE = {
    'provisao_ferias': u'Provisão de Férias',
    'adiantamento_13': u'Décimo Terceiro Salário',
    'decimo_terceiro': u'Décimo Terceiro Salário',
    'provisao_decimo_terceiro': u'Provisão de 13º',
    'normal': u'Folha normal',
}


class L10nBrHrPayslip(models.Model):
    _inherit = b'hr.payslip.run'

    account_event_id = fields.Many2one(
        string='Evento Contábil',
        comodel_name='account.event'
    )

    @api.multi
    def close_payslip_run(self):
        """
        Adicionar geração do evento contábil no fechamento do Lote de holerites

        """
        self.ensure_one()
        super(L10nBrHrPayslip, self).close_payslip_run()
        self.gerar_contabilizacao_lote()

    @api.multi
    def gerar_rubricas_para_lancamentos_contabeis_lote(self):
        """
        Gerar Lançamentos contábeis apartir do lote de holerites
        """
        self.ensure_one()

        # Dict para totalizar todas rubricas de todos holerites
        all_rubricas = {}

        for payslip in self.slip_ids:
            # Rubricas do holerite para contabilizar
            rubricas_holerite = payslip.gerar_contabilizacao_rubricas()

            for rubrica_holerite in rubricas_holerite:
                # EX.: rubrica_holerite = {'code': 'INSS', 'valor': 621.03}
                code = rubrica_holerite[2].get('code')
                valor = rubrica_holerite[2].get('valor')

                if code in all_rubricas:
                    # Somar rubrica do holerite ao dict totalizador
                    valor_total = \
                        all_rubricas.get(code)[2].get('valor') + valor
                    all_rubricas.get(code)[2].update(valor=valor_total)
                    line_id = \
                        rubrica_holerite[2].get('hr_payslip_line_id')[0][1]
                    all_rubricas.get(code)[2].get(
                        'hr_payslip_line_id').append((4, line_id))
                else:
                    all_rubricas[code] = rubrica_holerite

        return all_rubricas.values()

    @api.multi
    def gerar_contabilizacao_lote(self):
        """
        Processa a contabilização do lote baseado nas rubricas dos holerites
        """
        for lote in self:

            # Exclui o Evento Contábbil
            lote.account_event_id.unlink()

            rubricas = self.gerar_rubricas_para_lancamentos_contabeis_lote()

            contabiliz = {
                'account_event_line_ids': rubricas,
                'data': lote.data_de_pagamento or fields.Date.today(),
                'tipo': lote.tipo_de_folha,
                'company_id': lote.company_id.id,
                'ref': '{} - {:02}/{}'.format(
                    NOME_LANCAMENTO_LOTE.get(lote.tipo_de_folha),
                    lote.mes_do_ano, lote.ano),
                'origem': '{},{}'.format('hr.payslip.run', lote.id),
            }

            lote.account_event_id =\
                self.env['account.event'].create(contabiliz)

    @api.multi
    def gerar_codigo_contabilizacao(self):
        """
        Se o lote ja tiver sido processado, os códigos contabeis das rubricas
        nao foram processados. Essa função atualiza as linhas dos holerites do
        lote com o código contabil de cada rubrica
        """
        for record in self:
            for holerite_id in record.slip_ids:
                holerite_id.gerar_codigo_contabilizacao()
