# -*- coding: utf-8 -*-
#
# Copyright 2019 ABGF - Luiz Felipe do Divino <luiz.divino@abgf.gov.br>
# License AGPL-3 or later (http://www.gnu.org/licenses/agpl)
#

from openerp import api, fields, models, _
from openerp.exceptions import Warning

LATERALIDADE = [
    ('0', 'Não Aplicável'),
    ('1', 'Esquerda'),
    ('2', 'Direita'),
    ('3', 'Ambas'),
]


class HrAcidenteParteAtingida(models.Model):
    _name = 'hr.acidente.parte.atingida'
    _description = u'Partes Atingidas no Acidente'

    name = fields.Char(
        string=u'Nome Condição',
        compute='_compute_name',
    )
    contract_id = fields.Many2one(
        string=u'Contrato de Trabalho',
        comodel_name='hr.contract',
        domain=[('situacao_esocial', '=', 1)]
    )
    cod_parte_atingida = fields.Many2one(
        string=u'Código Parte Atingida',
        comodel_name='sped.parte_corpo',
    )
    lateralidade = fields.Selection(
        string=u'Lateralidade',
        selection=LATERALIDADE,
    )
    acidente_trabalho_id = fields.Many2one(
        comodel_name='hr.comunicacao.acidente.trabalho',
    )

    @api.model
    def _compute_name(self):
        for record in self:
            record.name = '{} - {} - {}'.format(
                record.data_acidente, record.contract_id.name,
                record.tipo_acidente.nome
            )
