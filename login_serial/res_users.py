from openerp.addons.product.product import sanitize_ean13
from openerp import api, exceptions, _
from openerp.models import Model
import random


MAX_RETRY_FOR_GENERATE_SERIAL_ID = 10000


def generate_serial_id():
    serial_id = ''
    for x in range(12):
        serial_id += str(int(random.random() * 10))
    return sanitize_ean13(serial_id)


class res_users(Model):
    _name = 'res.users'
    _inherit = 'res.users'

    @api.model
    def _get_fresh_serial_id(self):
        for x in range(MAX_RETRY_FOR_GENERATE_SERIAL_ID):
            serial_id = generate_serial_id()
            if not self.search([('serial_id', '=', serial_id)]):
                return serial_id
        raise exceptions.Warning(
            _('Cannot generate Serial Id'),
            _(
                'Odoo was unable to generate a fresh random Serial Id.' +
                ' It may be that there are a big amount of Serial Id' +
                ' already generated. You can try again.'
            )
        )

    @api.multi
    def generate_fresh_serial_id(self):
        for record in self:
            record.serial_id = record._get_fresh_serial_id()
