
from django.core.management.base import BaseCommand
from salons.models import Region
import pycountry

class Command(BaseCommand):
    help = "Seed the Region table with all countries using pycountry"

    def handle(self, *args, **options):
        count = 0
        for country in pycountry.countries:
            obj, created = Region.objects.get_or_create(
                country_code=country.alpha_2,
                defaults={
                    "name": country.name,
                    "currency": "USD",  # you could enhance later with forex API
                    "language": "en"    # you could enhance later with language mapping
                }
            )
            if created:
                count += 1

        self.stdout.write(self.style.SUCCESS(f"Seeded {count} regions into the database."))
