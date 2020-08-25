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
    INDICATIVO_FORMA_PAGAMENTO,
    TIPO_MOVIMENTO,
    TIPO_SERVICO,
)

_logger = logging.getLogger(__name__)


class AccountPaymentOrder(models.Model):
    _inherit = 'account.payment.order'

    def _confirm_debit_orders_api(self):
        """
        Method create to confirm all bank_api exclusive account.payment.order
        :return:
        """
        _logger.info('_confirm_debit_orders_api()')

        order_ids = self.search(
            [('active', '=', False), ('state', '=', 'draft'), ('name', 'ilike', 'api')]
        )

        for order_id in order_ids:
            try:
                order_id.draft2open()
                order_id.active = True
            except Exception as e:
                _logger.warn(str(e))
