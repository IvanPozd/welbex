from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import random
import string


class Cargo(models.Model):
    pick_up_location = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='pick_up_cargos')
    delivery_location = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='delivery_cargos')
    weight = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)])
    description = models.TextField()

    def __str__(self):
        return self.description

class Location(models.Model):
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f"{self.city}, {self.state} {self.zip_code}"

class Car(models.Model):
    unique_number = models.CharField(max_length=5, unique=True)
    current_location = models.ForeignKey('Location', on_delete=models.CASCADE)
    payload_capacity = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)])

    def __str__(self):
        return self.unique_number

    def save(self, *args, **kwargs):
        if not self.unique_number:
            self.unique_number = self.generate_unique_number()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_unique_number():
        digits = random.randint(1000, 9999)
        letter = random.choice(string.ascii_uppercase)
        return f"{digits}{letter}"
