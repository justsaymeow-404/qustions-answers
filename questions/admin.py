from django.contrib import admin

from .models import Question, Answer

@admin.register(Question)
class QustionAdmin(admin.ModelAdmin):
    fields = ('text', )


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    fields = ('question', 'user_id', 'text')