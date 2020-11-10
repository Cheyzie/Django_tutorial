from django.contrib import admin
from .models import Choice, Question
# Register your models here.
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Информация о дате создания', {'fields' : ['pub_date', 'active_days']})
    ]
    list_display = ('question_text', 'pub_date', 'was_published_recently', 'is_active')
    list_filter = ['pub_date']
    search_fields = ['question_text']
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)