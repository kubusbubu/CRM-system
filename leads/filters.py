import django_filters
from .models import Lead

class LeadFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='exact')

    class Meta:
        model = Lead
        fields = ['category']
