from django import forms
from django.utils import timezone
from datetime import datetime
from .models import Habit, HabitLog
from django.utils.text import slugify
from unidecode import unidecode

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['title', 'description', 'target']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание',
                'rows': 3
            }),
            'target': forms.NumberInput(attrs={
                'class': 'form-control-number',
                'type': 'number',
                'min': 1,
                'step': 1
            }),
        }
        labels = {
            'title': 'Название привычки',
            'description': 'Описание привычки',
            'target': 'Сколько выполнить в день',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title or not self.user:
            return title
        
        slug = slugify(f'{unidecode(title)}-{self.user.id}')
        if not slug:
            return title
        
        habit_in_db = Habit.objects.filter(user=self.user, slug=slug)
        if self.instance.pk:
            habit_in_db = habit_in_db.exclude(pk=self.instance.pk)
        
        if habit_in_db.exists():
            raise forms.ValidationError('У вас уже есть привычка с таким названием')
        
        return title

    def clean_target(self):
        target = self.cleaned_data.get('target')
        if target is not None:
            if target < 1:
                raise forms.ValidationError('Цель на день не может быть меньше 1')
        return target


class HabitLogForm(forms.ModelForm):
    #переопределяем поле модели datetime чтобы оно принимало только время, а дату подставим сегодняшнюю
    datetime = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        label='Введите время'
    )
    class Meta:
        model = HabitLog
        fields = ['datetime']
        

    def clean_datetime(self):
        time = self.cleaned_data.get('datetime')
        date_today = timezone.localdate()
        dt = timezone.make_aware(
            datetime.combine(date_today, time)
        )
        
        return dt