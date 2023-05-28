from django.test import TestCase, Client
from django.forms import ValidationError
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from .models import Cargo, Location, Car
from .serializers import LocationSerializer, CargoSerializer
from .views import LocationViewSet

class TransportModelsTestCase(TestCase):
    def setUp(self):
        self.location1 = Location.objects.create(
            city='Los Angeles',
            state='California',
            zip_code='90001',
            latitude='34.0522',
            longitude='-118.2437'
        )
        self.location2 = Location.objects.create(
            city='San Francisco',
            state='California',
            zip_code='94102',
            latitude='37.7749',
            longitude='-122.4194'
        )
        self.cargo = Cargo.objects.create(
            pick_up_location=self.location1,
            delivery_location=self.location2,
            weight=500,
            description='Sample cargo'
        )
        self.car = Car.objects.create(
            current_location=self.location1,
            payload_capacity=800
        )

    def test_location_str(self):
        self.assertEqual(str(self.location1), 'Los Angeles, California 90001')

    def test_cargo_str(self):
        self.assertEqual(str(self.cargo), 'Sample cargo')

    def test_car_str(self):
        self.assertEqual(len(str(self.car)), 6) # since this is generated string, check its length is correct

    def test_car_generate_unique_number(self):
        self.assertIsNotNone(Car.generate_unique_number())

    def test_car_save_with_unique_number(self):
        car = Car(current_location=self.location2, payload_capacity=900, unique_number='1234A')
        car.save()
        self.assertEqual(car.unique_number, '1234A')
        self.assertTrue(Car.objects.filter(unique_number='1234A').exists())

    def test_cargo_weight_validator(self):
        cargo = Cargo(pick_up_location=self.location1, delivery_location=self.location2, weight=2000, description='Sample cargo')
        with self.assertRaises(ValidationError):
            cargo.full_clean()
            
    def test_car_payload_capacity_validator(self):
        car = Car(current_location=self.location2, payload_capacity=0)
        with self.assertRaises(ValidationError):
            car.full_clean()


client = Client()
api_client = APIClient()

class CarViewSetTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.car = Car.objects.create(make="Toyota", model="Corolla", year=2020)

    def test_car_viewset_retrieve(self):
        response = api_client.get(f"/cars/{self.car.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["make"], "Toyota")
        self.assertEqual(response.data["model"], "Corolla")
        self.assertEqual(response.data["year"], 2020)

    def test_car_viewset_update(self):
        data = {"make": "Toyota", "model": "Camry", "year": 2021}
        response = api_client.put(f"/cars/{self.car.id}/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_car = Car.objects.get(id=self.car.id)
        self.assertEqual(updated_car.make, "Toyota")
        self.assertEqual(updated_car.model, "Camry")
        self.assertEqual(updated_car.year, 2021)

    def test_car_viewset_list(self):
        response = api_client.get("/cars/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["make"], "Toyota")
        self.assertEqual(response.data[0]["model"], "Corolla")
        self.assertEqual(response.data[0]["year"], 2020)

class LocationViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.viewset = LocationViewSet.as_view({'get': 'list'})
        self.locations = [Location.objects.create(name=f'Location {i+1}') for i in range(3)]

    def test_locations_list(self):
        response = self.client.get('/locations/')
        serialized_data = LocationSerializer(self.locations, many=True).data
        self.assertEqual(response.data, serialized_data)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        for location in self.locations:
            location.delete()
            

class GetAllCargosTest(APITestCase):
    """ Test module for GET all cargos API """

    def setUp(self):
        Cargo.objects.create(
            pick_up_location='Sample Pick Up Location',
            delivery_location='Sample Delivery Location',
            weight=50,
            description='Sample Cargo Description'
        )
        Cargo.objects.create(
            pick_up_location='Sample Pick Up Location 2',
            delivery_location='Sample Delivery Location 2',
            weight=40,
            description='Sample Cargo Description 2'
        )

    def test_get_all_cargos(self):
        # get API response
        response = client.get(reverse('cargo-list'))
        # get data from db
        cargos = Cargo.objects.all()
        serializer = CargoSerializer(cargos, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetSingleCargoTest(APITestCase):
    """ Test module for GET single cargo API """

    def setUp(self):
        self.cargo1 = Cargo.objects.create(
            pick_up_location='Sample Pick Up Location',
            delivery_location='Sample Delivery Location',
            weight=50,
            description='Sample Cargo Description'
        )
        self.cargo2 = Cargo.objects.create(
            pick_up_location='Sample Pick Up Location 2',
            delivery_location='Sample Delivery Location 2',
            weight=40,
            description='Sample Cargo Description 2'
        )

    def test_get_valid_single_cargo(self):
        response = client.get(
            reverse('cargo-detail', kwargs={'pk': self.cargo1.pk}))
        cargo = Cargo.objects.get(pk=self.cargo1.pk)
        serializer = CargoSerializer(cargo)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_cargo(self):
        response = client.get(
            reverse('cargo-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class CreateNewCargoTest(APITestCase):
    """ Test module for creating a new cargo """

    def setUp(self):
        self.valid_payload = {
            'pick_up_location': 'Sample Pick Up Location',
            'delivery_location': 'Sample Delivery Location',
            'weight': 50,
            'description': 'Sample Cargo Description',
        }
        self.invalid_payload = {
            'pick_up_location': '',
            'delivery_location': '',
            'weight': 50,
            'description': 'Sample Cargo Description',
        }

    def test_create_valid_cargo(self):
        response = client.post(
            reverse('cargo-list'),
            data=self.valid_payload,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_cargo(self):
        response = client.post(
            reverse('cargo-list'),
            data=self.invalid_payload,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
