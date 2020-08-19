# © 2012 KMEE INFORMATICA LTDA
#   @author Luis Felipe Mileo <mileo@kmee.com.br>
#   @author Daniel Sadamo <daniel.sadamo@kmee.com.br>
#   @author Fernando Marcato <fernando.marcato@kmee.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


{
    'name': 'Account Payment CNAB API',
    'version': '12.0.1.0.0',
    'category': 'Banking addons',
    'license': 'AGPL-3',
    'author': 'KMEE, Odoo Community Association (OCA)',
    'website': 'http://github.com/OCA/l10n-brazil',
    'depends': ['l10n_br_account_payment_order'],
    'data': [
        # Security
        'security/ir.model.access.csv',

        # Views
        'views/res_company.xml',
        'views/account_invoice.xml',
        'views/bank_api_operation_views.xml',

        # Wizards
        'wizards/account_invoice_api_confirm.xml',
    ],
    'installable': False,
    'auto_install': False,
}
