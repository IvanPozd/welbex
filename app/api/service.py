
import django_filters.rest_framework as filters
from geopy.distance import geodesic
from .models import Cargo, Car



class CargoFilter(filters.FilterSet):
    nearest_distance = filters.NumberFilter(method='filter_nearest_distance', label="Nearest distance")

    def filter_nearest_distance(self, queryset, name, value):
        
        car_location = self.request.query_params.get('current_location')
        if car_location:
            nearest_cargos = []
            for cargo in queryset:
                distance = geodesic((cargo.pick_up_location.latitude, cargo.pick_up_location.longitude),
                                    (car_location.latitude, cargo.pick_up_location.longitude)).miles
                if distance <= value:
                    nearest_cargos.append(cargo.id)
            
            return queryset.filter(id__in=nearest_cargos)
        
        return queryset
    
    class Meta:
        model = Cargo
        fields = ['nearest_distance']