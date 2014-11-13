from datetime import datetime
import logging

from openerp.addons.product.product import check_ean
from openerp.tests.common import TransactionCase


log = logging.getLogger(__name__)


class TestSerialLogin(TransactionCase):

    def setUp(self):
        super(TestSerialLogin, self).setUp()
        self.user_pool = self.registry('res.users')

    def create_user(self, **vals):
        return self.user_pool.create(self.cr, self.uid, vals)

    def get_user(self, user_id):
        return self.user_pool.browse(self.cr, self.uid, user_id)[0]

    def get_new_user_name(self):
        return 'user_' + datetime.now().strftime("%y%m%d%H%M%S%f")

    def test_serial_id_is_unique_on_create(self):
        name = self.get_new_user_name()
        serial_id = '5012345678900'
        self.create_user(name=name, login=name, serial_id=serial_id)
        new_name = self.get_new_user_name()
        with self.assertRaises(Exception):
            self.create_user(
                name=new_name, login=new_name, serial_id=serial_id
            )

    def test_serial_id_is_unique_on_write(self):
        name = self.get_new_user_name()
        serial_id = '5012345678900'
        self.create_user(name=name, login=name, serial_id=serial_id)

        new_name = self.get_new_user_name()
        new_serial_id = '7501054530107'
        new_user_id = self.create_user(
            name=new_name, login=new_name, serial_id=new_serial_id
        )
        with self.assertRaises(Exception):
            self.user_pool.write(
                self.cr, self.uid, new_user_id, {'serial_id': serial_id}
            )

    def test_create_generates_valid_ean(self):
        name = self.get_new_user_name()
        user_id = self.create_user(name=name, login=name)
        user = self.get_user(user_id)
        self.assertTrue(user.serial_id)
        self.assertTrue(
            check_ean(user.serial_id),
            'The user\'s Serial Id is not a valid EAN-13 code.'
        )

