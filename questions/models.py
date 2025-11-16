from django.db import models

import uuid


class Question(models.Model):
    text = models.TextField(verbose_name='Вопрос', null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'Вопрос №{self.id}'
    

class Answer(models.Model):
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE, related_name='answers')
    user_id = models.UUIDField()
    text = models.TextField(verbose_name='Ответ')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
    
    def __str__(self):
        return f'Ответ №{self.id} на вопрос №{self.question_id}'
