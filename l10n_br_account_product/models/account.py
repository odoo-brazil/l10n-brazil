# -*- coding: utf-8 -*-
# Copyright (C) 2009 - TODAY Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from datetime import datetime

from odoo import models, fields, api


class AccountPaymentTerm(models.Model):
    _inherit = 'account.payment.term'

    indPag = fields.Selection(
        [('0', u'Pagamento à Vista'), ('1', u'Pagamento à Prazo'),
         ('2', 'Outros')], 'Indicador de Pagamento', default='1')


class AccountTaxTemplate(models.Model):
    """Implement computation method in taxes"""
    _inherit = 'account.tax.template'

    domain = fields.Char('Domain', size=8)
    icms_base_type = fields.Selection(
        [('0', 'Margem Valor Agregado (%)'), ('1', 'Pauta (valor)'),
         ('2', 'Preço Tabelado Máximo (valor)'),
         ('3', 'Valor da Operação')],
        'Tipo Base ICMS', required=True, default='0')
    icms_st_base_type = fields.Selection(
        [('0', 'Preço tabelado ou máximo  sugerido'),
         ('1', 'Lista Negativa (valor)'),
         ('2', 'Lista Positiva (valor)'), ('3', 'Lista Neutra (valor)'),
         ('4', 'Margem Valor Agregado (%)'), ('5', 'Pauta (valor)')],
        'Tipo Base ICMS ST', required=True, default='4')


class AccountTax(models.Model):
    """Implement computation method in taxes"""
    _inherit = 'account.tax'

    icms_base_type = fields.Selection(
        [('0', 'Margem Valor Agregado (%)'), ('1', 'Pauta (valor)'),
         ('2', 'Preço Tabelado Máximo (valor)'),
         ('3', 'Valor da Operação')],
        'Tipo Base ICMS', required=True, default='0')
    icms_st_base_type = fields.Selection(
        [('0', 'Preço tabelado ou máximo  sugerido'),
         ('1', 'Lista Negativa (valor)'),
         ('2', 'Lista Positiva (valor)'), ('3', 'Lista Neutra (valor)'),
         ('4', 'Margem Valor Agregado (%)'), ('5', 'Pauta (valor)')],
        'Tipo Base ICMS ST', required=True, default='4')

    def _compute_tax(self, taxes, total_line, product, product_qty,
                     precision, base_tax=0.0):
        result = {'tax_discount': 0.0, 'taxes': []}

        for tax in taxes:
            if tax.get('type') == 'weight' and product:
                product_read = self.env['product.product'].read(
                   product, ['weight_net'])
                tax['amount'] = round((product_qty * product_read.get(
                    'weight_net', 0.0)) * tax['percent'], precision)

            if base_tax:
                total_line = base_tax

            if tax.get('type') == 'quantity':
                tax['amount'] = round(product_qty * tax['percent'], precision)

            tax['amount'] = round(total_line * tax['percent'], precision)
            tax['amount'] = round(tax['amount'] * (1 - tax['base_reduction']),
                                  precision)

            if tax.get('tax_discount'):
                result['tax_discount'] += tax['amount']

            if tax['percent']:
                unrounded_base = total_line * (1 - tax['base_reduction'])
                tax['total_base'] = round(unrounded_base, precision)
                tax['total_base_other'] = round(total_line - tax['total_base'],
                                                precision)
            else:
                tax['total_base'] = 0.00
                tax['total_base_other'] = 0.00

        result['taxes'] = taxes
        return result


    #TODO
    #TODO MIG V10
    # Refatorar este método, para ficar mais simples e não repetir
    # o que esta sendo feito no método l10n_br_account_product
    @api.multi
    def compute_all(self, price_unit, currency=None, quantity=1.0, product=None, partner=None,
                    force_excluded=False, fiscal_position=False,
                    insurance_value=0.0, freight_value=0.0,
                    other_costs_value=0.0, base_tax=0.00):
        """Compute taxes

        Returns a dict of the form::

        {
            'total': Total without taxes,
            'total_included': Total with taxes,
            'total_tax_discount': Total Tax Discounts,
            'taxes': <list of taxes, objects>,
            'total_base': Total Base by tax,
        }
        """
        if len(self) == 0:
            company_id = self.env.user.company_id
        else:
            company_id = self[0].company_id
        if not currency:
            currency = company_id.currency_id
        obj_precision = self.env['decimal.precision']
        precision = obj_precision.precision_get('Account')
        result = super(AccountTax, self).compute_all(price_unit, currency=currency, quantity=quantity, product=product, partner=partner)
        totaldc = icms_value = 0.0
        ipi_value = 0.0
        calculed_taxes = []

        for tax in result['taxes']:
            tax_list = [tx for tx in self if tx.id == tax['id']]
            if tax_list:
                tax_brw = tax_list[0]
            tax['domain'] = tax_brw.domain
            tax['type'] = tax_brw.amount_type
            tax['percent'] = tax_brw.amount
            tax['base_reduction'] = tax_brw.base_reduction
            tax['amount_mva'] = tax_brw.amount_mva
            tax['tax_discount'] = tax_brw.tax_discount

            if tax.get('domain') == 'icms':
                tax['icms_base_type'] = tax_brw.icms_base_type

            if tax.get('domain') == 'icmsst':
                tax['icms_st_base_type'] = tax_brw.icms_st_base_type

        common_taxes = [tx for tx in result['taxes'] if tx[
            'domain'] not in ['icms', 'icmsst', 'ipi']]
        result_tax = self._compute_tax(common_taxes, result['total_excluded'],
                                       product, quantity, precision, base_tax)
        totaldc += result_tax['tax_discount']
        calculed_taxes += result_tax['taxes']

        # Calcula o IPI
        specific_ipi = [tx for tx in result['taxes'] if tx['domain'] == 'ipi']
        result_ipi = self._compute_tax(specific_ipi,result['total_excluded'],
                                       product, quantity, precision, base_tax)
        totaldc += result_ipi['tax_discount']
        calculed_taxes += result_ipi['taxes']
        for ipi in result_ipi['taxes']:
            ipi_value += ipi['amount']

        # Calcula ICMS
        specific_icms = [tx for tx in result['taxes']
                         if tx['domain'] == 'icms']
        if fiscal_position and fiscal_position.asset_operation:
            total_base =result['total_excluded'] + insurance_value + \
                freight_value + other_costs_value + ipi_value
        else:
            total_base =result['total_excluded'] + insurance_value + \
                freight_value + other_costs_value

        result_icms = self._compute_tax(
            specific_icms,
            total_base,
            product,
            quantity,
            precision,
            base_tax)
        totaldc += result_icms['tax_discount']
        calculed_taxes += result_icms['taxes']
        if result_icms['taxes']:
            icms_value = result_icms['taxes'][0]['amount']

        # Calcula ICMS ST
        specific_icmsst = [tx for tx in result['taxes']
                           if tx['domain'] == 'icmsst']
        result_icmsst = self._compute_tax(specific_icmsst,
                                         result['total_excluded'], product,
                                          quantity, precision, base_tax)
        totaldc += result_icmsst['tax_discount']
        if result_icmsst['taxes']:
            icms_st_percent = result_icmsst['taxes'][0]['percent']
            icms_st_percent_reduction = result_icmsst[
                'taxes'][0]['base_reduction']
            icms_st_base = round(((result['total_excluded'] + ipi_value) *
                                 (1 - icms_st_percent_reduction)) *
                                 (1 + result_icmsst['taxes'][0]['amount_mva']),
                                 precision)
            icms_st_base_other = round(
                ((result['total_excluded'] + ipi_value) * (
                    1 + result_icmsst['taxes'][0]['amount_mva'])),
                precision) - icms_st_base
            result_icmsst['taxes'][0]['total_base'] = icms_st_base
            result_icmsst['taxes'][0]['amount'] = round(
                (icms_st_base * icms_st_percent) - icms_value, precision)
            result_icmsst['taxes'][0]['icms_st_percent'] = icms_st_percent
            result_icmsst['taxes'][0][
                'icms_st_percent_reduction'] = icms_st_percent_reduction
            result_icmsst['taxes'][0][
                'icms_st_base_other'] = icms_st_base_other

            if result_icmsst['taxes'][0]['percent']:
                calculed_taxes += result_icmsst['taxes']

        # Estimate Taxes
        if fiscal_position and fiscal_position.asset_operation:
            obj_tax_estimate = self.env['l10n_br_tax.estimate']
            date = datetime.now().strftime('%Y-%m-%d')
            tax_estimate_ids = obj_tax_estimate.search(
                cr, uid, [('fiscal_classification_id', '=',
                           product.fiscal_classification_id.id),
                          '|', ('date_start', '=', False),
                          ('date_start', '<=', date),
                          '|', ('date_end', '=', False),
                          ('date_end', '>=', date),
                          ('active', '=', True)])

            if tax_estimate_ids:
                tax_estimate = obj_tax_estimate.browse(
                    tax_estimate_ids)[0]
                tax_estimate_percent = 0.00
                if product.origin in ('1', '2', '6', '7'):
                    tax_estimate_percent += tax_estimate.federal_taxes_import
                else:
                    tax_estimate_percent += tax_estimate.federal_taxes_national

                tax_estimate_percent += tax_estimate.state_taxes
                tax_estimate_percent /= 100
                total_taxes = ((result['total_included'] - totaldc) *
                               tax_estimate_percent)
                result['total_taxes'] = round(total_taxes, precision)

        return {
            'total': result['total_excluded'],
            'total_included': result.get('total_included', 0.00),
            'total_tax_discount': totaldc,
            'taxes': calculed_taxes,
            'total_taxes': result.get('total_taxes', 0.00),
        }


