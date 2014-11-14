import logging
import random

from openerp import SUPERUSER_ID
from openerp.addons.product.product import check_ean, sanitize_ean13
from openerp.osv import fields, osv


MAX_RETRY_FOR_GENERATE_SERIAL_ID = 10000


def generate_serial_id():
    serial_id = ''
    for _ in range(12):
        serial_id += str(int(random.random() * 10))
    return sanitize_ean13(serial_id)


class res_users(osv.osv):
    _name = 'res.users'
    _inherit = 'res.users'
    _columns = {
        'serial_id': fields.char('Serial Id')
    }

    _sql_constraints = [
        (
            'serial_id_unique',
            'unique(serial_id)',
            'There is another user with this Serial Id.'
        )
    ]

    def check_credentials(self, cr, uid, password):
        res = self.search(
            cr, SUPERUSER_ID,
            [('id', '=', uid), ('serial_id', '=', password)])
        if res:
            return res
        super(res_users, self).check_credentials(cr, uid, password)

    def _validate_serial_id(self, vals):
        if 'serial_id' in vals and not check_ean(vals['serial_id']):
            raise osv.except_osv(
                'Serial Id invalid format',
                'The Serial Id field has not the EAN-13 format standard.'
            )

    def _get_fresh_serial_id(self, cr, uid, context=None):
        for _ in range(MAX_RETRY_FOR_GENERATE_SERIAL_ID):
            serial_id = generate_serial_id()
            if not self.search(
                cr, uid, [('serial_id', '=', serial_id)], context=context
            ):
                return serial_id
        raise osv.except_osv(
            'Cannot generate Serial Id',
            'Odoo was unable to generate a fresh random Serial Id.' +
            ' It may be that there are a big amount of Serial Id' +
            ' already generated. You can try again.'
        )

    def create(self, cr, uid, vals, context=None):
        if 'serial_id' in vals:
            self._validate_serial_id(vals)
        else:
            vals['serial_id'] = self._get_fresh_serial_id(
                cr, uid, context=context
            )
        return super(res_users, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        self._validate_serial_id(vals)
        return super(res_users, self).write(
            cr, uid, ids, vals, context=context
        )

    def generate_fresh_serial_ids(self, cr, uid, ids, context=None):
        for id in ids:
            serial_id = self._get_fresh_serial_id(cr, uid, context=context)
            self.write(
                cr, uid, id, {'serial_id': serial_id}, context=context
            )
