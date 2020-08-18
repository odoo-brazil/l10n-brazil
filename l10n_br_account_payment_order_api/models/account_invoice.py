#    @author Danimar Ribeiro <danimaribeiro@gmail.com>
# © 2012 KMEE INFORMATICA LTDA
#   @author Luis Felipe Mileo <mileo@kmee.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    bank_api_operation_ids = fields.One2many(
        string='Operações Realizadas',
        comodel_name='bank.api.operation',
        inverse_name='invoice_id',
        readonly=True,
    )

    def register_invoice_api(self):
        """ Registrar o boleto via sua API"""
        raise NotImplementedError

    def create_bank_api_operation(self, request, operation_type=False,
                                  environment=False):
        # 'not request' não é válido para o propósito
        if request == False:
            return

        operation_model = self.env["bank.api.operation"]

        if not operation_type:
            operation_type = "post"

        data = {
            "operation_type": operation_type,
            "invoice_id": self.id,
            "environment": environment,
        }

        operation_id = operation_model.create(data)
        operation_id.register_post(request)
        self.bank_api_operation_ids += operation_id

    @api.multi
    def create_api_account_payment_line(self):
        # TODO: Criar CRON para confirmar as account.payment.order no final de
        #  cada dia
        apoo = self.env["account.payment.order"]
        result_payorder_ids = []
        payorder = False
        for inv in self:
            if inv.state != "open":
                raise UserError(_("The invoice %s is not in Open state") % inv.number)
            if not inv.move_id:
                raise UserError(_("No Journal Entry on invoice %s") % inv.number)
            applicable_lines = inv.move_id.line_ids.filtered(
                lambda x: (
                    not x.reconciled
                    and x.payment_mode_id.payment_order_ok
                    and x.account_id.internal_type in ("receivable", "payable")
                    and not x.payment_line_ids
                )
            )
            if not applicable_lines:
                raise UserError(
                    _(
                        "No Payment Line created for invoice %s because "
                        "it already exists or because this invoice is "
                        "already paid."
                    )
                    % inv.number
                )
            payment_modes = applicable_lines.mapped("payment_mode_id")
            if not payment_modes:
                raise UserError(_("No Payment Mode on invoice %s") % inv.number)
            for payment_mode in payment_modes:
                payorder = apoo.search(
                    [
                        ("payment_mode_id", "=", payment_mode.id),
                        ("state", "=", "draft"),
                        ("active", "=", False),
                        ("name", "ilike", "api"),
                    ],
                    limit=1,
                )

                new_payorder = False
                if not payorder:
                    payorder = apoo.create(
                        inv._prepare_new_payment_order(payment_mode)
                    )
                    new_payorder = True
                    payorder.name += "_api"
                    payorder.active = False

                result_payorder_ids.append(payorder.id)
                count = 0
                for line in applicable_lines.filtered(
                    lambda x: x.payment_mode_id == payment_mode
                ):
                    line.create_payment_line_from_move_line(payorder)
                    count += 1
                if new_payorder:
                    inv.message_post(
                        _(
                            "%d payment lines added to the new draft payment "
                            "order %s which has been automatically created."
                        )
                        % (count, payorder.name)
                    )
                else:
                    inv.message_post(
                        _(
                            "%d payment lines added to the existing draft "
                            "payment order %s."
                        )
                        % (count, payorder.name)
                    )
        return payorder
