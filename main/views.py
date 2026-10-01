from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.db.models import Q, F, Count, When, Case, Value, BooleanField
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils import timezone

from .models import Habit, HabitLog
from .forms import HabitForm, HabitLogForm


class HabitListView(LoginRequiredMixin, ListView):
    model = Habit
    template_name = 'main/habit/list.html'
    context_object_name = 'habits'
    paginate_by = 12

    def get_queryset(self):
        today = timezone.localdate()
        queryset = Habit.objects.filter(user=self.request.user).annotate(
            count_done = Count('habit_logs', filter=Q(habit_logs__datetime__date=today))
        ).annotate(
            is_done = Case(
                When(count_done__gte=F('target'), then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        )

        query = self.request.GET.get('q', '')
        if query:
            queryset = queryset.filter(Q(title__icontains=query))

        filter_param = self.request.GET.get('filter', '')
        if filter_param == 'active':
            queryset = queryset.filter(is_active=True)
        if filter_param == 'inactive':
            queryset = queryset.filter(is_active=False)
        if filter_param == 'done':
            queryset = queryset.filter(is_done=True)
        if filter_param == 'not_done':
            queryset = queryset.filter(is_done=False)

        sort_options = {
            'title': 'title',
            '-title': '-title',
            'new': '-created_at',
            'old': 'created_at',
            'active': '-is_active',
            'inactive': 'is_active',
            'done': '-is_done',
            'not_done': 'is_done',
        }
        sort_param = self.request.GET.get('sort', '')
        order_by = sort_options.get(sort_param, 'title')
        queryset = queryset.order_by(order_by)

        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['filter'] = self.request.GET.get('filter', '')
        context['sort'] = self.request.GET.get('sort', '')
        return context


class HabitDetailView(LoginRequiredMixin, DetailView):
    model = Habit
    template_name = 'main/habit/detail.html'
    context_object_name = 'habit'
    slug_field = 'slug'
    slug_url_kwarg = 'habit_slug'

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()
        habit = self.get_object()
        today_logs = habit.habit_logs.filter(datetime__date=today)
        is_done = today_logs.exists() and today_logs.count() >= habit.target
        context['today_logs'] = today_logs
        context['is_done'] = is_done
        context['form'] = HabitLogForm()
        return context


class HabitCreateView(LoginRequiredMixin, CreateView):
    model = Habit
    form_class = HabitForm
    template_name = 'main/habit/form.html'
    success_url = reverse_lazy('main:habit_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание привычки'
        context['button_text'] = 'Создать'
        return context


class HabitUpdateView(LoginRequiredMixin, UpdateView):
    model = Habit
    form_class = HabitForm
    template_name = 'main/habit/form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'habit_slug'

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('main:habit_detail', kwargs={'habit_slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование привычки'
        context['button_text'] = 'Сохранить'
        return context


class HabitDeleteView(LoginRequiredMixin, DeleteView):
    model = Habit
    template_name = 'main/habit/confirm_delete.html'
    success_url = reverse_lazy('main:habit_list')
    slug_field = 'slug'
    slug_url_kwarg = 'habit_slug'

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, f'Привычка "{self.object.title}" удалена.')
        return super().delete(request, *args, **kwargs)


@login_required
@require_POST
def habit_reverse_is_active(request, habit_slug):
    habit = get_object_or_404(Habit, slug=habit_slug, user=request.user)
    habit.is_active = not habit.is_active
    habit.save(update_fields=['is_active'])
    return redirect('main:habit_detail', habit_slug=habit_slug)


class HabitLogCreateView(LoginRequiredMixin, CreateView):
    model = HabitLog
    form_class = HabitLogForm
    template_name = 'main/habit_log/form.html'

    def form_valid(self, form):
        habit = get_object_or_404(
            Habit,
            slug=self.kwargs.get('habit_slug'),
            user=self.request.user
        )
        form.instance.habit = habit
        return super().form_valid(form)

    def form_invalid(self, form):
        print('ERRORS', form.errors)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('main:habit_detail', kwargs={'habit_slug': self.kwargs.get('habit_slug')})


class HabitLogDeleteView(LoginRequiredMixin, DeleteView):
    model = HabitLog
    template_name = 'main/habit_log/confirm_delete.html'

    def get_object(self, queryset = None):
        return get_object_or_404(
            HabitLog,
            pk=self.kwargs.get('log_id'),
            habit__slug=self.kwargs.get('habit_slug'),
            habit__user=self.request.user
        )

    def delete(self, request, *args, **kwargs):
        messages.success(request, f'Отметка привычки "{self.object.habit.title}" удалена.')
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('main:habit_detail', kwargs={'habit_slug': self.kwargs.get('habit_slug')})


class UserRegisterView(FormView):
    template_name = 'main/user/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('main:habit_list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:habit_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        messages.success(self.request, f'Аккаунт {username} успешно создан. Теперь вы можете войти.')
        return super().form_valid(form)
