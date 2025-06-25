from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Habit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    place = models.CharField(max_length=255, verbose_name='Место')
    time = models.TimeField(verbose_name='Время')
    action = models.CharField(max_length=255, verbose_name='Действие')
    is_pleasant = models.BooleanField(default=False, verbose_name='Приятная привычка')
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Связанная привычка',
        limit_choices_to={'is_pleasant': True}
    )
    periodicity = models.PositiveIntegerField(default=1, verbose_name='Периодичность (в днях)')
    reward = models.CharField(max_length=255, blank=True, null=True, verbose_name='Вознаграждение')
    execution_time = models.PositiveIntegerField(verbose_name='Время выполнения (в секундах)')
    is_public = models.BooleanField(default=False, verbose_name='Публичная')

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'

    def __str__(self):
        return f'{self.action} в {self.time} в {self.place}'

    def clean(self):
        # ❌ Одновременно указаны и вознаграждение, и связанная привычка
        if self.reward and self.related_habit:
            raise ValidationError("Нельзя одновременно указывать вознаграждение и связанную привычку.")

        # ⏱ Время выполнения > 120 секунд
        if self.execution_time > 120:
            raise ValidationError("Время выполнения привычки не должно превышать 120 секунд.")

        # ✅ Связанная привычка должна быть помечена как приятная
        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError("Связанная привычка должна быть приятной.")

        # 🚫 У приятной привычки не может быть вознаграждения или связанной привычки
        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError("Приятная привычка не может иметь вознаграждение или связанную привычку.")

        # 🔁 Периодичность < 1 или > 7
        if self.periodicity < 1 or self.periodicity > 7:
            raise ValidationError("Периодичность должна быть от 1 до 7 дней.")

    def save(self, *args, **kwargs):
        self.full_clean()  # запускает clean() перед сохранением
        super().save(*args, **kwargs)
