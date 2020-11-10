from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
class Question(models.Model):
    question_text = models.CharField('Текст вопроса', max_length=200)
    pub_date = models.DateTimeField('Дата публикации')
    active_days = models.IntegerField('Продолжительность(дней)', default=7)

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_active(self):
        now = timezone.now()
        return now - datetime.timedelta(days=self.active_days) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    is_active.boolean = True
    is_active.short_description = 'Активный?'
    was_published_recently.short_description = 'Недавно опубликовано?'

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.choice_text
