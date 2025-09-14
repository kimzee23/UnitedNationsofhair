from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Create a staff user (company staff)"

    def add_arguments(self, parser):
        parser.add_argument("--email", type=str, required=True, help="Staff email")
        parser.add_argument("--username", type=str, required=True, help="Staff username")
        parser.add_argument("--password", type=str, default="staff123", help="Staff password")
        parser.add_argument("--phone", type=str, default=None, help="Phone number (optional)")

    def handle(self, *args, **options):
        email = options["email"]
        username = options["username"]
        password = options["password"]
        phone = options.get("phone")

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f"Staff with email {email} already exists."))
            return

        user = User.objects.create_user(
            email=email,
            username=username,
            phone=phone,
            password=password,
            is_staff=True,
            is_verified=True
        )

        self.stdout.write(self.style.SUCCESS(f"Staff {user.username} created successfully."))
