from django.utils import timezone
from rest_framework import viewsets, filters, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, F, Count, When, Case, Value, BooleanField
from django.shortcuts import get_object_or_404

from .serializers import HabitSerializer, HabitLogSerializer
from .permissions import IsAuthenticated, IsHabitOwnerOrStaff, IsHabitLogOwnerOrStaff
from ..models import Habit, HabitLog
from .filters import HabitFilter


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    permission_classes = [IsAuthenticated, IsHabitOwnerOrStaff]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = HabitFilter
    search_fields = ['title']
    ordering_fields = ['title', 'created_at', 'is_active', 'is_done']
    ordering = ['title']

    def get_queryset(self):
        queryset = Habit.objects.filter(user=self.request.user).annotate(
            count_done=Count('habit_logs', filter=Q(habit_logs__datetime__date=timezone.localdate()))
        ).annotate(
            is_done=Case(
                When(count_done__gte=F('target'), then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        )
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['POST'], serializer_class=serializers.Serializer)
    def reverse_active(self, request, slug=None):
        habit = get_object_or_404(Habit, slug=slug, user=request.user)
        habit.is_active = not habit.is_active
        habit.save(update_fields=['is_active'])
        if habit.is_active:
            return Response({'status': 'Привычка возобновлена'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Привычка приостановлена'}, status=status.HTTP_200_OK)


class HabitLogViewSet(viewsets.ModelViewSet):
    serializer_class = HabitLogSerializer
    permission_classes = [IsAuthenticated, IsHabitLogOwnerOrStaff]
    # Логи нельзя редактировать — только создавать и удалять
    http_method_names = ['get', 'post', 'delete', 'head', 'options']

    def get_queryset(self):
        habit_slug = self.kwargs.get('habit_slug')
        return HabitLog.objects.filter(
            habit__user=self.request.user,
            habit__slug=habit_slug
        )

    def perform_create(self, serializer):
        habit = get_object_or_404(
            Habit,
            slug=self.kwargs.get('habit_slug'),
            user=self.request.user
        )
        serializer.save(habit=habit)