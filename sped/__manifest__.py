# -*- coding: utf-8 -*-
#
# Copyright 2016 Taŭga Tecnologia
#    Aristides Caldeira <aristides.caldeira@tauga.com.br>
# License AGPL-3 or later (http://www.gnu.org/licenses/agpl)
#

{
    'name': u'SPED',
    'version': '10.0.1.0.0',
    'author': u'Odoo Community Association (OCA), Ari Caldeira',
    'category': u'Base',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'document',
        'mail',
        'decimal_precision',
        'product',
        'sped_imposto',
    ],
    'installable': True,
    'application': True,
    'data': [
        #
        # Valores padrão
        #


        #
        # Menus principais
        #
        'views/cadastro_view.xml',





        #
        # Módulo Cadastro: participantes, produtos etc.
        #

        'views/sped_produto_produto_view.xml',
        'views/sped_unidade_produto_view.xml',

        'views/sped_produto_servico_view.xml',
        'views/sped_unidade_servico_view.xml',

        #
        # Parcelamentos e pagamentos
        #
        'views/sped_account_payment_term_line_view.xml',
        'views/sped_account_payment_term_view.xml',

        #
        # Fiscal
        #
        'views/sped_veiculo_view.xml',

        'views/sped_documento_item_declaracao_importacao_view.xml',
        'views/sped_documento_item_emissao_view.xml',

        'views/sped_documento_referenciado_view.xml',
        'views/sped_documento_pagamento_view.xml',

        'views/sped_documento_base_view.xml',

        'views/sped_documento_emissao_nfe_view.xml',
        'views/sped_documento_emissao_nfce_view.xml',
        # 'views/sped_documento_recebimento_nfe_view.xml',
    ],
    'external_dependencies': {
        'python': ['pybrasil'],
    }
}
