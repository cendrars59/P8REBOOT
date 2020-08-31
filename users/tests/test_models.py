from django.test import TestCase

from users.models import User


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create(
            username='dummy_user_name',
            email='Dummy@email.com',
            password='dummy_pwd_1',
        )

    def test_username(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('username')
        self.assertEquals(field_label, 'username')

    def test_email(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('dummy_user_name')
        self.assertEquals(field_label, 'Dummy@email.com')

    def test_pwd1(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('password')
        self.assertEquals(field_label, 'password')

