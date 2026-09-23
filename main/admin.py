from django.contrib import admin
from .models import Habit, HabitLog

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'is_active', 'description', 'created_at']
    prepopulated_fields = {'slug': ('title', )}
    list_filter = ['title', 'is_active', 'created_at']
    list_editable = ['title', 'is_active', 'description']
    search_fields = ['title']
    list_display_links = ('slug', )

@admin.register(HabitLog)
class HabitLogAdmin(admin.ModelAdmin):
    list_display = ['habit', 'datetime']
    list_filter = ['habit', 'datetime']
    list_display_links = ('datetime', )


