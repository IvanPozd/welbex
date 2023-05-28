import random
from django.core.management.base import BaseCommand
from api.models import Car, Location

class Command(BaseCommand):
    help = 'Create 20 machines with random locations'

    def handle(self, *args, **options):
        locations = Location.objects.all()
        if len(locations) < 20:
            raise ValueError("There are not enough locations in the database.")

        for i in range(20):
            location = random.choice(locations)
            machine = Car(
                current_location=location,
                payload_capacity=random.randint(1, 1000)
            )
            machine.save()
            self.stdout.write(self.style.SUCCESS(f"Created Car with unique number: {machine.unique_number}"))
