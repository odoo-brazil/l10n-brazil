
from openerp import models, api, fields

# entender como usar
class PaymentMode(models.Model):
    _inherit = "payment.mode"

    domain = fields.Char('Domain', default="[('id','in',[])]")

    @api.multi
    def _get_domain(self):
        self.ensure_one()
        return self.id

# Conferir adaptacao para account.invoice
class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    payment_mode_domain = fields.Char(
        related='payment_mode_id.domain', string='Payment Mode Domain',
        store=True)

    # terminar alteracoes
    @api.multi
    def onchange_partner_id(self, partner_id):
        res = super(AccountInvoice, self).onchange_partner_id(partner_id)
        partner_obj = self.env['res.partner'].browse(partner_id)

        domain = self._mount_domain(partner_obj, self.amount_total)
        res['value']['payment_mode_domain'] = domain['payment_mode_domain']

        return res

    # Nao necessario
    @api.multi
    def button_dummy(self):
        self.ensure_one()
        ret = super(AccountInvoice, self).button_dummy()
        self.payment_term = False
        domain = self._mount_domain(
            self.partner_id, amount_total=self.amount_total)

        self.write({
            'payment_mode_domain': domain['payment_mode_domain'],
        })
        return ret

    # verificar visao <field name="payment_mode_id"
    #            domain="[('domain', '=', payment_mode_domain)]"/>
    # código já adaptado
    @api.multi
    def _mount_domain(self, partner_obj, amount_total):
        payment_mode_ids = []
        line = self.env['account.payment.mode'].search([
            ('liquidity', '=', False)])
        if amount_total > partner_obj.available_credit_limit:
            payment_mode_ids.append(line.payment_mode)
        else:
            line = self.env['account.payment.mode'].search([
                ('liquidity', '=', True)])
            payment_mode_ids.append(line.payment_mode)

        payment_mode_domain = "[('id','in',%s)]" % str(payment_mode_ids)

        for mode in payment_mode_ids:
            mode.write({'domain': payment_mode_domain})

        return {'payment_mode_domain': payment_mode_domain}
