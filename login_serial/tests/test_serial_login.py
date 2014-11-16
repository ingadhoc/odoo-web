from datetime import datetime
import time

from openerp import exceptions
from openerp.addons.product.product import check_ean
from openerp.addons.login_serial.res_users import generate_serial_id
from openerp.tests.common import TransactionCase


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

    def test_serial_id_should_be_valid_ean13(self):
        name = self.get_new_user_name()
        invalid_serial_id = '5012345678901'
        serial_id = '5012345678900'

        with self.assertRaises(exceptions.Warning):
            self.create_user(
                name=name, login=name, serial_id=invalid_serial_id
            )

        user_id = self.create_user(name=name, login=name, serial_id=serial_id)
        with self.assertRaises(exceptions.Warning):
            self.user_pool.write(
                self.cr, self.uid, user_id, {'serial_id': invalid_serial_id}
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

    def test_generate_serial_id_are_valid_ean(self):
        for _ in range(1000):
            serial_id = generate_serial_id()
            self.assertTrue(
                check_ean(serial_id),
                'The generate Serial Id "{0}" is not a valid EAN-13'.format(
                    serial_id
                )
            )

    def test_generate_fresh_serial_ids(self):
        name_1 = self.get_new_user_name()
        user_id_1 = self.create_user(name=name_1, login=name_1)

        time.sleep(1)
        name_2 = self.get_new_user_name()
        user_id_2 = self.create_user(name=name_2, login=name_2)

        self.user_pool.write(
            self.cr, self.uid, [user_id_1, user_id_2], {'serial_id': None}
        )
        self.user_pool.generate_fresh_serial_ids(
            self.cr, self.uid, [user_id_1, user_id_2]
        )

        user_1 = self.user_pool.browse(self.cr, self.uid, user_id_1)
        user_2 = self.user_pool.browse(self.cr, self.uid, user_id_2)
        for user in [user_1, user_2]:
            self.assertTrue(user.serial_id)
            self.assertTrue(
                check_ean(user.serial_id),
                'The generate Serial Id "{0}" is not a valid EAN-13'.format(
                    user.serial_id
                )
            )
