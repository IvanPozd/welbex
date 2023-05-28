import csv
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import Location

class Command(BaseCommand):
    help = 'Loads unique locations from uszips.csv into the database'

    def handle(self, *args, **options):
        file_path = os.path.abspath('uszips.csv')  # Update with the actual file path
        
        with open(file_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            
            with transaction.atomic():
                Location.objects.all().delete()  # Clear existing locations
                
                for row in reader:
                    location = Location(
                        city=row['city'],
                        state=row['state_name'],
                        zip_code=row['zip'],
                        latitude=row['lat'],
                        longitude=row['lng']
                    )
                    location.save()
        
        self.stdout.write(self.style.SUCCESS('Locations loaded successfully.'))
