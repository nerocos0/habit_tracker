from django.utils import timezone
from datetime import datetime

from rest_framework import serializers
from ..models import Habit, HabitLog

class HabitSerializer(serializers.ModelSerializer):
    count_done = serializers.IntegerField(read_only=True)
    is_done = serializers.BooleanField(read_only=True)

    class Meta:
        model = Habit
        fields = ['id', 'title', 'slug', 'description', 'target', 'created_at', 'is_active', 'count_done', 'is_done']
        read_only_fields = ['id', 'slug', 'created_at', 'is_active']

    def create(self, validated_data):
        date = timezone.localdate()
        return Habit.objects.create(created_at=date, **validated_data)


class HabitLogSerializer(serializers.ModelSerializer):
    time_input = serializers.TimeField(write_only=True, required=True)
    time_output = serializers.SerializerMethodField()

    class Meta:
        model = HabitLog
        fields = ['id', 'habit', 'time_input', 'time_output']
        read_only_fields = ['id', 'habit', 'datetime']

    def create(self, validated_data):
        time = validated_data.pop('time_input')
        date = timezone.localdate()
        dt = timezone.make_aware(
            datetime.combine(date, time)
        )
        return HabitLog.objects.create(datetime=dt, **validated_data)

    def get_time_output(self, obj):
        if obj.datetime:
            time = timezone.localtime(obj.datetime)
            return time.strftime('%H:%M')
        return None
