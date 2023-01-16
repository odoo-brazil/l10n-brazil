# Copyright 2023 KMEE
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PosInvoiceCancelReason(models.Model):

    _name = "pos.invoice.cancel.reason"
    _description = "POS Invoice Cancel Reason"

    name = fields.Char(
        string="Name",
        required=True,
    )

    active = fields.Boolean(
        string="Active",
        default=False,
    )
