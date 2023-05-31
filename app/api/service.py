
import django_filters.rest_framework as filters
from geopy.distance import geodesic
from .models import Cargo, Car



class CargoFilter(filters.FilterSet):
    weight = filters.NumberFilter(method='filter_weight', label="Weight")

    def filter_weight(self, queryset, value, view):
        return queryset.filter(weight__lte=value)
        
    class Meta:
        model = Cargo
        fields = ['weight']