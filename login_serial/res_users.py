import logging

from openerp import SUPERUSER_ID
from openerp.osv import fields, osv


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
