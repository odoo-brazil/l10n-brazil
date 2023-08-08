# © 2023 KMEE INFORMATICA LTDA (https://kmee.com.br)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import base64
import calendar
import logging
import os
from datetime import datetime

import pytz

from odoo import _, fields, models
from odoo.exceptions import RedirectWarning

_logger = logging.getLogger(__name__)

try:
    from erpbrasil.base import misc
except ImportError:
    _logger.error("Biblioteca erpbrasil.base não instalada")


class FiscalClosing(models.Model):
    _inherit = "l10n_br_fiscal.closing"

    document_cfe_pos_ids = fields.One2many(
        comodel_name="pos.order",
        string="CFe POS Documents",
        inverse_name="close_id",
    )

    def _prepare_files(self, temp_dir):
        temp_dir = super(FiscalClosing, self)._prepare_files(temp_dir)
        date_range = calendar.monthrange(int(self.year), int(self.month))
        date_min = datetime(
            int(self.year),
            int(self.month),
            1,
            0,
            0,
            1,
            tzinfo=pytz.timezone(self.env.context["tz"]),
        ).astimezone(pytz.utc)
        date_max = datetime(
            int(self.year),
            int(self.month),
            date_range[1],
            23,
            59,
            59,
            tzinfo=pytz.timezone(self.env.context["tz"]),
        ).astimezone(pytz.utc)
        orders = self.env["pos.order"].search(
            [
                ("company_id", "=", self.company_id.id),
                ("date_order", ">=", date_min),
                ("date_order", "<=", date_max),
                ("state", "not in", ["draft"]),
                ("amount_paid", ">=", 0),
                ("authorization_file", "!=", False),
            ]
        )

        document_path = "/".join(
            [misc.punctuation_rm(self.company_id.cnpj_cpf), "cfe_pos"]
        )

        for order in orders:
            try:
                filename = os.path.join(
                    temp_dir, document_path, f"{order.document_key}.xml"
                )
                if not os.path.exists(os.path.dirname(filename)):
                    os.makedirs(os.path.dirname(filename))

                with open(filename, "wb") as file:
                    file.write(base64.b64decode(order.authorization_file))

                if order.cancel_document_key:
                    filename = os.path.join(
                        temp_dir, document_path, f"{order.cancel_document_key}.xml"
                    )
                    if not os.path.exists(os.path.dirname(filename)):
                        os.makedirs(os.path.dirname(filename))

                    with open(filename, "wb") as file:
                        file.write(base64.b64decode(order.cancel_file))
            except OSError as e:
                raise RedirectWarning(_("Error!"), _("I/O Error")) from e
            except PermissionError as e:
                raise RedirectWarning(
                    _("Error!"), _("Check write permissions in your system temp folder")
                ) from e
            except Exception:
                _logger.error(
                    _(
                        "Replication failed: document attachments "
                        "[id = {}] is not present in the database."
                    ).format(order.name)
                )

        self.write({"document_cfe_pos_ids": [(6, 0, orders.ids)]})

        return temp_dir
