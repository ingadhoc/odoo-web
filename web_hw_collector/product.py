from openerp import fields,  _
from openerp.models import Model


class product_template(Model):

    _name = 'product.template'
    _inherit = 'product.template'

    measured_weight = fields.Float(string=_('Measured Weight'))
