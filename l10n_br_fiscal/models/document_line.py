# Copyright (C) 2013  Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models
from ..constants.icms import ICMS_BASE_TYPE, ICMS_BASE_TYPE_DEFAULT


class DocumentLine(models.Model):
    _name = "l10n_br_fiscal.document.line"
    _inherit = "l10n_br_fiscal.document.line.abstract"
    _description = "Fiscal Document Line"

    @api.model
    def _default_operation(self):
        # TODO add in res.company default Operation?
        return self.env['l10n_br_fiscal.operation']

    @api.model
    def _operation_domain(self):
        domain = [('state', '=', 'approved')]
        return domain

    operation_id = fields.Many2one(
        default=_default_operation,
        domain=lambda self: self._operation_domain())

    document_id = fields.Many2one(
        comodel_name="l10n_br_fiscal.document", string="Document")

    icms_base_type = fields.Selection(
        selection=ICMS_BASE_TYPE,
        string="ICMS Base Type",
        default=ICMS_BASE_TYPE_DEFAULT,
    )

    def _onchange_all(self):
        self._onchange_product_id()
        self._onchange_commercial_quantity()
        self._onchange_ncm_id()
        self._onchange_operation_id()
        self._onchange_operation_line_id()
        self._onchange_fiscal_taxes()
