from openerp import fields, _
from openerp.models import Model


class product_product(Model):
    _name = 'product.product'
    _inherit = 'product.product'

    collected_number = fields.Integer(string=_('Collected Number'))
