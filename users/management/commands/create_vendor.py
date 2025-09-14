from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from vendor.models import VendorApplication

User = get_user_model()


class Command(BaseCommand):
    help = "Create a vendor user (and vendor application record)"

    def add_arguments(self, parser):
        parser.add_argument("--email", type=str, required=True, help="Vendor email")
        parser.add_argument("--username", type=str, required=True, help="Vendor username")
        parser.add_argument("--password", type=str, default="vendor123", help="Vendor password")
        parser.add_argument("--phone", type=str, default=None, help="Phone number (optional)")
        parser.add_argument("--country", type=str, default="NG", help="Vendor country (default NG)")

    def handle(self, *args, **options):
        email = options["email"]
        username = options["username"]
        password = options["password"]
        phone = options.get("phone")
        country = options.get("country")

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f"Vendor with email {email} already exists."))
            return

        user = User.objects.create_user(
            email=email,
            username=username,
            phone=phone,
            password=password,
            role=User.Role.VENDOR,
            is_verified=True,
            country=country,
            application_status=User.ApplicationStatus.APPROVED,
            application_role=User.Role.VENDOR,
        )

        VendorApplication.objects.create(
            user=user,
            status="APPROVED",
            business_certificate="auto-approved",
            nin="auto-approved"
        )

        self.stdout.write(self.style.SUCCESS(f"Vendor {user.username} created successfully."))
