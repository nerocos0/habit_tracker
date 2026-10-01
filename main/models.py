from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from unidecode import unidecode

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    target = models.PositiveIntegerField(default=1)
    created_at = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'title'], name='unique_user_habit')
        ]
        ordering = ['title']
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if (not self.slug) or (not slugify(unidecode(self.title)) == self.slug):
            transliterated_title = unidecode(self.title)
            slug = f'{transliterated_title}-{self.user_id}'
            self.slug = slugify(slug)
        super().save(*args, **kwargs)

class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='habit_logs')
    datetime = models.DateTimeField()

    class Meta:
        ordering = ['-datetime']
        verbose_name = 'Выполнение привычки'
        verbose_name_plural = 'Выполнение привычек'

    def __str__(self):
        return f'{self.habit.title} - {self.datetime}'