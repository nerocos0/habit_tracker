import django_filters
from ..models import Habit

class HabitFilter(django_filters.FilterSet):
    is_done = django_filters.BooleanFilter(field_name='is_done')

    class Meta:
        model = Habit
        fields = ['is_active']