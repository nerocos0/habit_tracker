from django import forms
from django.utils import timezone
from datetime import datetime
from .models import Habit, HabitLog

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