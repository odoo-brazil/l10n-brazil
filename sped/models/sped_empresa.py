# -*- coding: utf-8 -*-
#
# Copyright 2016 Taŭga Tecnologia
#   Aristides Caldeira <aristides.caldeira@tauga.com.br>
# License AGPL-3 or later (http://www.gnu.org/licenses/agpl)
#

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.addons.l10n_br_base.constante_tributaria import (
    AMBIENTE_NFE,
    INDICADOR_IE_DESTINATARIO_CONTRIBUINTE,
    REGIME_TRIBUTARIO_LUCRO_PRESUMIDO,
    REGIME_TRIBUTARIO_LUCRO_REAL,
    REGIME_TRIBUTARIO_SIMPLES,
    REGIME_TRIBUTARIO_SIMPLES_EXCESSO,
    TIPO_EMISSAO_NFE,
)
import logging

_logger = logging.getLogger(__name__)


try:
    from email_validator import validate_email

    from pybrasil.base import mascara, primeira_maiuscula
    from pybrasil.inscricao import (
        formata_cnpj, formata_cpf, limpa_formatacao,
        formata_inscricao_estadual, valida_cnpj, valida_cpf,
        valida_inscricao_estadual
    )
    from pybrasil.telefone import (
        formata_fone, valida_fone_fixo, valida_fone_celular,
        valida_fone_internacional
    )

except (ImportError, IOError) as err:
    _logger.debug(err)


class Empresa(models.Model):
    _description = u'Empresas e filiais'
    _inherit = 'sped.empresa'

    #
    # Para o faturamento
    #
    protocolo_id = fields.Many2one(
        comodel_name='sped.protocolo.icms',
        string=u'Protocolo padrão',
        ondelete='restrict',
        domain=[('tipo', '=', 'P')]
    )
    simples_anexo_id = fields.Many2one(
        comodel_name='sped.aliquota.simples.anexo',
        string=u'Anexo do SIMPLES',
        ondelete='restrict')
    simples_teto_id = fields.Many2one(
        comodel_name='sped.aliquota.simples.teto',
        string=u'Teto do SIMPLES',
        ondelete='restrict')
    simples_aliquota_id = fields.Many2one(
        comodel_name='sped.aliquota.simples.aliquota',
        string=u'Alíquotas do SIMPLES',
        ondelete='restrict',
        compute='_compute_simples_aliquota_id')
    simples_anexo_servico_id = fields.Many2one(
        comodel_name='sped.aliquota.simples.anexo',
        string=u'Anexo do SIMPLES (produtos)',
        ondelete='restrict')
    simples_aliquota_servico_id = fields.Many2one(
        comodel_name='sped.aliquota.simples.aliquota',
        string=u'Alíquotas do SIMPLES (serviços)',
        ondelete='restrict',
        compute='_compute_simples_aliquota_id')
    al_pis_cofins_id = fields.Many2one(
        comodel_name='sped.aliquota.pis.cofins',
        string=u'Alíquota padrão do PIS-COFINS',
        ondelete='restrict'
    )
    operacao_produto_id = fields.Many2one(
        comodel_name='sped.operacao',
        string=u'Operação padrão para venda',
        ondelete='restrict',
        domain=[
            ('modelo', 'in', ('55', '65', '2D')),
            ('emissao', '=', '0')
        ])
    operacao_produto_pessoa_fisica_id = fields.Many2one(
        comodel_name='sped.operacao',
        string=u'Operação padrão para venda pessoa física',
        ondelete='restrict',
        domain=[('modelo', 'in', ('55', '65', '2D')), ('emissao', '=', '0')]
    )
    operacao_produto_ids = fields.Many2many(
        'sped.operacao',
        'res_partner_sped_operacao_produto',
        'partner_id',
        'operacao_id',
        string=u'Operações permitidas para venda',
        domain=[
            ('modelo', 'in', ('55', '65', '2D')),
            ('emissao', '=', '0')
        ])
    operacao_servico_id = fields.Many2one(
        comodel_name='sped.operacao',
        string=u'Operação padrão para venda',
        ondelete='restrict',
        domain=[('modelo', 'in', ('SE', 'RL')), ('emissao', '=', '0')]
    )
    operacao_servico_ids = fields.Many2many(
        'sped.operacao',
        'res_partner_sped_operacao_servico',
        'partner_id',
        'operacao_id',
        string=u'Operações permitidas para venda',
        domain=[('modelo', 'in', ('SE', 'RL')), ('emissao', '=', '0')]
    )

    @api.depends(
        'simples_anexo_id', 'simples_anexo_servico_id', 'simples_teto_id')
    def _compute_simples_aliquota_id(self):
        for empresa in self:
            simples_aliquota_ids = self.env[
                'sped.aliquota.simples.aliquota'].search([
                    ('anexo_id', '=', empresa.simples_anexo_id.id),
                    ('teto_id', '=', empresa.simples_teto_id.id),
                ])

            if len(simples_aliquota_ids) != 0:
                empresa.simples_aliquota_id = simples_aliquota_ids[0]
            else:
                empresa.simples_aliquota_id = False

            simples_aliquota_ids = self.env[
                'sped.aliquota.simples.aliquota'].search([
                    ('anexo_id', '=', empresa.simples_anexo_servico_id.id),
                    ('teto_id', '=', empresa.simples_teto_id.id),
                ])

            if len(simples_aliquota_ids) != 0:
                empresa.simples_aliquota_servico_id = simples_aliquota_ids[0]
            else:
                empresa.simples_aliquota_servico_id = False

    @api.onchange('regime_tributario')
    def onchange_regime_tributario(self):
        valores = {}
        res = {'value': valores}

        if self.regime_tributario == REGIME_TRIBUTARIO_SIMPLES:
            valores.update(al_pis_cofins_id=self.env.ref(
                'sped.ALIQUOTA_PIS_COFINS_SIMPLES').id)

        elif self.regime_tributario == REGIME_TRIBUTARIO_SIMPLES_EXCESSO:
            valores.update(al_pis_cofins_id=self.env.ref(
                'sped.ALIQUOTA_PIS_COFINS_LUCRO_PRESUMIDO').id)

        elif self.regime_tributario == REGIME_TRIBUTARIO_LUCRO_PRESUMIDO:
            valores.update(al_pis_cofins_id=self.env.ref(
                'sped.ALIQUOTA_PIS_COFINS_LUCRO_PRESUMIDO').id)

        elif self.regime_tributario == REGIME_TRIBUTARIO_LUCRO_REAL:
            valores.update(al_pis_cofins_id=self.env.ref(
                'sped.ALIQUOTA_PIS_COFINS_LUCRO_REAL').id)

        return res