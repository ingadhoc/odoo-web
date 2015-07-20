from datetime import datetime

from openerp import exceptions
from openerp.addons.product.product import check_ean
from openerp.addons.login_serial.res_users import generate_serial_id
from openerp.tests.common import TransactionCase


class TestSerialLogin(TransactionCase):

    def setUp(self):
        super(TestSerialLogin, self).setUp()
        self.user_model = self.env['res.users']

    def create_user(self, **vals):
        return self.user_model.create(vals)

    def get_new_user_name(self):
        return 'user_' + datetime.now().strftime("%y%m%d%H%M%S%f")

    def test_check_credentials_using_serial_id(self):
        name = self.get_new_user_name()
        user = self.create_user(name=name, login=name)
        user_id = user.sudo(user.id).check_credentials(user.serial_id)
        self.assertTrue(user_id)

    def test_serial_id_is_unique_on_create(self):
        name = self.get_new_user_name()
        user = self.create_user(name=name, login=name)
        new_name = self.get_new_user_name()
        with self.assertRaises(Exception):
            self.create_user(
                name=new_name, login=new_name, serial_id=user.serial_id
            )

    def test_serial_id_is_unique_on_write(self):
        name_1 = self.get_new_user_name()
        # user_1 = self.create_user(name=name_1, login=name_1)
        name_2 = self.get_new_user_name()
        user_2 = self.create_user(name=name_2, login=name_2)
        with self.assertRaises(Exception):
            name_1.serial_id = user_2.serial_id

    def test_serial_id_should_be_valid_ean13(self):
        name = self.get_new_user_name()
        invalid_serial_id = '5012345678901'
        with self.assertRaises(exceptions.Warning):
            self.create_user(
                name=name, login=name, serial_id=invalid_serial_id
            )

        user = self.create_user(name=name, login=name)
        with self.assertRaises(exceptions.Warning):
            user.serial_id = invalid_serial_id

    def test_create_generates_valid_ean(self):
        name = self.get_new_user_name()
        user = self.create_user(name=name, login=name)
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

    def test_generate_fresh_serial_id(self):
        name_1 = self.get_new_user_name()
        user_1 = self.create_user(name=name_1, login=name_1)
        name_2 = self.get_new_user_name()
        user_2 = self.create_user(name=name_2, login=name_2)

        user_1.serial_id = None
        user_2.serial_id = None
        user_1.generate_fresh_serial_id()
        user_2.generate_fresh_serial_id()

        for user in [user_1, user_2]:
            self.assertTrue(user.serial_id)
            self.assertTrue(
                check_ean(user.serial_id),
                'The generate Serial Id "{0}" is not a valid EAN-13'.format(
                    user.serial_id
                )
            )
