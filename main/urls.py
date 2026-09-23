from django.urls import path
from .views import (HabitListView, HabitDetailView, HabitCreateView, HabitUpdateView, HabitDeleteView,
                    HabitLogCreateView, HabitLogDeleteView, UserRegisterView,
                    habit_reverse_is_active)
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'main'

urlpatterns = [
    path('', HabitListView.as_view(), name='habit_list'),
    path('habit/create/', HabitCreateView.as_view(), name='habit_create'),
    path('habit/<slug:habit_slug>/', HabitDetailView.as_view(), name='habit_detail'),
    path('habit/<slug:habit_slug>/update/', HabitUpdateView.as_view(), name='habit_update'),
    path('habit/<slug:habit_slug>/delete/', HabitDeleteView.as_view(), name='habit_delete'),
    path('habit/<slug:habit_slug>/reverse/', habit_reverse_is_active, name='habit_reverse'),
    path('habit/<slug:habit_slug>/logs/create/', HabitLogCreateView.as_view(), name='habit_log_create'), 
    path('habit/<slug:habit_slug>/logs/<int:log_id>/delete/', HabitLogDeleteView.as_view(), name='habit_log_delete'),
    path('login/', LoginView.as_view(template_name='main/user/login.html', next_page='main:habit_list'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
]