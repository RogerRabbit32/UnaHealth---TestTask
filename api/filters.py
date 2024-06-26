import django_filters
from .models import GlucoseLevel


class GlucoseLevelFilter(django_filters.FilterSet):

    user_id = django_filters.NumberFilter(
        field_name='user__id',
    )

    start = django_filters.DateTimeFilter(
        field_name='timestamp',
        lookup_expr='gte',
    )

    stop = django_filters.DateTimeFilter(
        field_name='timestamp',
        lookup_expr='lte',
    )

    class Meta:
        model = GlucoseLevel
        fields = ['user_id', 'start', 'stop']
