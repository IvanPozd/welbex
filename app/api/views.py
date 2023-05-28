from django_filters.rest_framework import DjangoFilterBackend
from .models import Car, Cargo, Location
from geopy.distance import geodesic
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from .serializers import CarSerializer, LocationSerializer, CargoSerializer
from .service import CargoFilter


class CarViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
    ):
    serializer_class = CarSerializer
    queryset = Car.objects.all().order_by("id")
    lookup_field = "id"


class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()


class CargoViewSet(viewsets.ModelViewSet):
    serializer_class = CargoSerializer
    filter_backends = [DjangoFilterBackend]
    #filterset_class = CargoFilter
    
    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        try:
            cargo = Cargo.objects.get(pk=pk)
        except:
            return Response(
                data={"error": f"Груза с индексом {pk} не существует"},
                status=status.HTTP_404_NOT_FOUND
                )
        machines = Car.objects.all()
        cars_near_cargo =[]
        for car in machines:
            distanse = geodesic(
                    (cargo.pick_up_location.latitude, cargo.pick_up_location.longitude),
                    (car.current_location.latitude, car.current_location.longitude)
                    ).miles
            car_dict = CarSerializer(car).data
            car_dict["distanse"] = distanse
            
            cars_near_cargo.append(car_dict)

        cargo_serializer = self.get_serializer(cargo)
        

        response_data = {
            'cargo': cargo_serializer.data,
            'machines_near_cargo': cars_near_cargo
        }
        
        return Response(response_data)

    def get_queryset(self):
        all_cargos = Cargo.objects.all()
        all_cars = Car.objects.all()
        
        cargos = []

        for cargo in all_cargos:
            cars_near_cargo = []
            for car in all_cars:
                distanse = geodesic(
                    (cargo.pick_up_location.latitude, cargo.pick_up_location.longitude),
                    (car.current_location.latitude, car.current_location.longitude)
                    ).miles
                if distanse <= 455:
                    cars_near_cargo.append(CarSerializer(car).data)

            cargos.append({
                'id': cargo.id,
                'pick_up_location': str(cargo.pick_up_location),
                'delivery_location': str(cargo.delivery_location),
                'weight': cargo.weight,
                'description': cargo.description,
                'cars_near_cargo': f"{len(cars_near_cargo)}",
            })
        
        return cargos

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return Response(queryset)
    
    def update(self, request, *args, **kwargs):
        
        pk = kwargs.get("pk", None)
        try:
            cargo_instance = Cargo.objects.get(id=pk)
        except:
            return Response({"error": "Груза с таким индексом не существует"},status=status.HTTP_404_NOT_FOUND)
        
        serialize_data = self.serializer_class(data=request.data, instance=cargo_instance)
        if serialize_data.is_valid():
            serialize_data.save()
            return Response(serialize_data.data, status=status.HTTP_200_OK)
        else:
            return Response(serialize_data.errors, status=status.HTTP_400_BAD_REQUEST)
