from openerp.addons.product.product import check_ean, sanitize_ean13
from openerp import api, exceptions, fields,  _
from openerp.models import Model
import random


MAX_RETRY_FOR_GENERATE_SERIAL_ID = 10000


def generate_serial_id():
    serial_id = ''
    for x in range(12):
        serial_id += str(int(random.random() * 10))
    return sanitize_ean13(serial_id)


class res_partner(Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    serial_id = fields.Char(string=_('Serial Id'), readonly=True)

    _sql_constraints = [
        (
            'serial_id_unique',
            'unique(serial_id)',
            _('There is another user with this Serial Id.')
        )
    ]

    @api.model
    def check_credentials(self, password):
        users = self.sudo().search(
            [('id', '=', self.env.uid), ('serial_id', '=', password)]
        )
        if users:
            return users
        super(res_partner, self).check_credentials(password)

    @api.multi
    def _validate_serial_id(self, vals):
        if 'serial_id' in vals and not check_ean(vals['serial_id']):
            raise exceptions.Warning(
                _('Serial Id invalid format'),
                _('The Serial Id field has not the EAN-13 format standard.')
            )

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

    @api.model
    def create(self, vals):
        if 'serial_id' in vals:
            self._validate_serial_id(vals)
        else:
            serial_id = self._get_fresh_serial_id()
            vals['serial_id'] = serial_id
        return super(res_partner, self).create(vals)

    @api.multi
    def write(self, vals):
        self._validate_serial_id(vals)
        return super(res_partner, self).write(vals)

    @api.multi
    def generate_fresh_serial_id(self):
        for record in self:
            record.serial_id = record._get_fresh_serial_id()
