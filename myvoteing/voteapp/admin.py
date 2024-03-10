from django.contrib import admin
from .models import Question, Choice, Response

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'created_at')
    fieldsets = [
        (None, {'fields': ['question_text']}),
    ]
    inlines = [ChoiceInline]

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Response)
