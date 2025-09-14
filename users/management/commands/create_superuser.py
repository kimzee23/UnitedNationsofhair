from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Create a superuser if it does not already exist"

    def add_arguments(self, parser):
        parser.add_argument("--email", type=str, required=True, help="Superuser email")
        parser.add_argument("--username", type=str, required=True, help="Superuser username")
        parser.add_argument("--password", type=str, default="admin123", help="Superuser password")
        parser.add_argument("--phone", type=str, default=None, help="Phone number (optional)")

    def handle(self, *args, **options):
        email = options["email"]
        username = options["username"]
        password = options["password"]
        phone = options.get("phone")

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f"Superuser with email {email} already exists."))
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f"Superuser with username {username} already exists."))
            return

        User.objects.create_superuser(
            email=email,
            username=username,
            phone=phone,
            password=password
        )

        self.stdout.write(self.style.SUCCESS(f"Superuser {username} created successfully."))
