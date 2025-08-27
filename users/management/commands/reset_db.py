from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection
import sys


class Command(BaseCommand):
    help = "Reset the database (development only). Drops all tables & runs migrations."

    def handle(self, *args, **kwargs):
        if not settings.DEBUG:
            self.stdout.write(self.style.ERROR(
                "This command is disabled in production (DEBUG=False)."
            ))
            sys.exit(1)

        self.stdout.write(self.style.WARNING("Dropping all tables..."))

        with connection.cursor() as cursor:
            cursor.execute("DROP SCHEMA public CASCADE;")
            cursor.execute("CREATE SCHEMA public;")
            cursor.execute("GRANT ALL ON SCHEMA public TO postgres;")  # change if your user is different
            cursor.execute("GRANT ALL ON SCHEMA public TO public;")

        self.stdout.write(self.style.SUCCESS("Database schema reset."))

        from django.core.management import call_command
        call_command("migrate")
        self.stdout.write(self.style.SUCCESS("Migrations applied."))
