# -*- coding: utf-8 -*-
# Copyright 2020 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields


class L10nBrCnabOption(models.Model):
    _name = 'l10n_br.cnab.option'

    code = fields.Char(
        string='Code',
    )

    description = fields.Char(
        string='Description',
    )

    option_type = fields.Selection(
        string='Option Type',
        selection=[
            ("release_form", "Forma de Lançamento"),
            ("service_type", "Tipo de Serviço"),
            ("ted_finality_code", "Código Finalidade da TED"),
            ("doc_finality_code", "Código Finalidade da DOC"),
        ]
    )

    bank_id = fields.Many2one(
        comodel_name='res.bank',
    )

    @api.multi
    @api.depends('code', 'description')
    def name_get(self):
        result = []
        for record in self:
            result.append(
                (record.id, '%s - %s' % (record.code, record.description))
            )
        return result

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if name:
            recs = self.search([('code', '=', name)] + args, limit=limit)
        if not recs:
            recs = self.search(
                [('description', operator, name)] + args, limit=limit)
        return recs.name_get()
