from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .api_views import HabitViewSet, HabitLogViewSet

app_name = 'api_main'

#основной роутер для HabitViewSet
router = DefaultRouter()
router.register(r'habits', HabitViewSet, basename='habit')

#доп роутер для логов Habit
habit_router = NestedDefaultRouter(router, r'habits', lookup='habit')
habit_router.register(r'logs', HabitLogViewSet, basename='habit-logs')

urlpatterns = [
    #JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    #Swagger
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='api_main:schema'), name='swagger-ui'),

    #API routers
    path('', include(router.urls)),
    path('', include(habit_router.urls)),
]