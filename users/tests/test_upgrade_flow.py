from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import User


class RoleUpgradeFlowTests(APITestCase):
    def setUp(self):
        self.client: APIClient = APIClient()

        self.customer = User.objects.create_user(
            email="customer@tests.com",
            username="customer",
            password="pass1234",
            role=User.Role.CUSTOMER,
        )

        self.admin = User.objects.create_superuser(
            email="admin@tests.com",
            username="admin",
            password="adminpass",
        )

        # Endpoints
        self.apply_url = reverse("apply-upgrade")
        self.approve_url = lambda user_id: reverse("approve-upgrade", args=[user_id])
        self.reject_url = lambda user_id: reverse("reject-upgrade", args=[user_id])

    def test_customer_can_apply_for_influencer_upgrade(self):
        """Customer can apply to become an Influencer."""
        self.client.force_authenticate(user=self.customer)
        response = self.client.post(self.apply_url, {"requested_role": User.Role.INFLUENCER})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.customer.refresh_from_db()
        self.assertEqual(self.customer.application_role, User.Role.INFLUENCER)
        self.assertEqual(self.customer.application_status, User.ApplicationStatus.PENDING)

    def test_vendor_request_redirects_to_vendor_apply(self):
        """Vendor requests are redirected to vendor/apply form."""
        self.client.force_authenticate(user=self.customer)
        response = self.client.post(self.apply_url, {"requested_role": User.Role.VENDOR})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("redirect_url", response.data)
        self.assertIn("/vendor/apply", response.data["redirect_url"])

    def test_user_cannot_apply_twice_if_pending(self):
        """Customer cannot apply twice if already pending as Influencer."""
        self.client.force_authenticate(user=self.customer)
        self.client.post(self.apply_url, {"requested_role": User.Role.INFLUENCER})
        response = self.client.post(self.apply_url, {"requested_role": User.Role.INFLUENCER})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_can_approve_upgrade(self):
        """Admin can approve an Influencer request."""
        self.client.force_authenticate(user=self.customer)
        self.client.post(self.apply_url, {"requested_role": User.Role.INFLUENCER})

        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(self.approve_url(self.customer.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.customer.refresh_from_db()
        self.assertEqual(self.customer.role, User.Role.INFLUENCER)
        self.assertEqual(self.customer.application_status, User.ApplicationStatus.APPROVED)

    def test_admin_can_reject_upgrade(self):
        """Admin can reject an Influencer request."""
        self.client.force_authenticate(user=self.customer)
        self.client.post(self.apply_url, {"requested_role": User.Role.INFLUENCER})

        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(self.reject_url(self.customer.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.customer.refresh_from_db()
        self.assertEqual(self.customer.role, User.Role.CUSTOMER)  # stays the same
        self.assertEqual(self.customer.application_status, User.ApplicationStatus.REJECTED)

    def test_non_admin_cannot_approve_or_reject(self):
        """Non-admin cannot approve or reject upgrade requests."""
        self.client.force_authenticate(user=self.customer)
        self.client.post(self.apply_url, {"requested_role": User.Role.INFLUENCER})

        # Same customer tries to approve themselves
        self.client.force_authenticate(user=self.customer)
        response = self.client.patch(self.approve_url(self.customer.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
