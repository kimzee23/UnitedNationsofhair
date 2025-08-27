
from django.test import TestCase

from users.models import User


class UserModelTest(TestCase):
    def test_create_customer(self):
        user = User.objects.create_user(
            email="customerOne@gmail.com",
            username="customerOne",
            phone = "08225026778",
            password="pass1234"
        )
        self.assertEqual(user.role, User.Role.CUSTOMER)
        self.assertEqual(user.email, "customerOne@gmail.com")
        self.assertEqual(user.username, "customerOne")
        self.assertEqual(user.phone, "08225026778")
        self.assertTrue(user.check_password("pass1234"))
        self.assertEqual(user.role, User.Role.CUSTOMER)

