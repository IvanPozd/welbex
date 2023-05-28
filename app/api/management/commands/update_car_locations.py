from django.core.management.base import BaseCommand
from api.models import Car, Location
import time


class Command(BaseCommand):
    help = 'Update machine locations every 3 minutes'

    def handle(self, *args, **options):
        while True:
            # Get all machines
            machines = Car.objects.all()

            # Iterate over each machine
            for machine in machines:
                # Generate a random location
                random_location = Location.objects.order_by('?').first()

                # Update the machine's location
                machine.current_location = random_location
                machine.save()

            # Wait for 3 minutes before updating again
            time.sleep(180)