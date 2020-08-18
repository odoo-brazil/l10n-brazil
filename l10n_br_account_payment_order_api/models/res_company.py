# © 2012 KMEE INFORMATICA LTDA
#   @author Luis Felipe Mileo <mileo@kmee.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    client_id = fields.Char(
        string='ID do Cliente',
    )

    client_secret = fields.Char(
        string='Segredo',
    )

    itau_key = fields.Char(
        string='Chave'
    )

    api_endpoint = fields.Char(
        string='API ENDPOINT'
    )

    raiz_endpoint = fields.Char(
        string='RAIZ ENDPOINT',
    )

    api_itau_token = fields.Char(
        string='Itaú API Token',
        readonly=True,
    )

    api_itau_token_due_datetime = fields.Datetime(
        string='Validade do Token',
        readonly=True,
    )
