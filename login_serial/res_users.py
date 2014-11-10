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
