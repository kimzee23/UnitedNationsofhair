import os

import django
from django.test import TestCase

from users.models import User

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "UnitedNationsOfHair.settings")
# django.setup()


class UserModelTest(TestCase):
    def test_create_customer(self):
        user = User.objects.create_user(
            email="customerOne@gmail.com",
            username="customerOne",
            phone = "08225026092",
            password="pass1234"
        )
        self.assertEqual(user.role, User.Role.CUSTOMER)
        self.assertEqual(user.password, "pass1234")
        self.assertEqual(str(user), "customerOne@gmail.com (CUSTOMER)")
