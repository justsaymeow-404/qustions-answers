from __future__ import annotations

import logging

from typing import Any, Dict, Optional, Type

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.serializers import Serializer

from django.db.models import Prefetch, QuerySet

from .models import Question, Answer
from .serializers import (
    QuestionListSerializer,
    QuestionDetailSerializer,
    QuestionCreateSerializer,
    AnswerSerializer,
    AnswerCreateSerializer
)
from .services.answers import add_answer
from .utils.uid import UIDResult, get_or_create_uid


logger = logging.getLogger('questions')


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    http_method_names = ['get', 'post', 'delete']

    serializer_action_classes = {
        'list': QuestionListSerializer,
        'retrive': QuestionDetailSerializer,
        'create': QuestionCreateSerializer,
        'create_answer': AnswerCreateSerializer
    }

    def get_queryset(self) -> QuerySet[Question]:
        queryset = super().get_queryset()
        if self.action == 'retrive':
            return queryset.prefetch_related(
                Prefetch('answers', queryset=Answer.objects.order_by('created_at'))
            )
        return queryset
    
    def get_serializer_class(self) -> Type[Serializer]:
        return self.serializer_action_classes.get(self.action, QuestionListSerializer)
    
    def perform_create(self, serializer: QuestionCreateSerializer):
        question = serializer.save()
        logger.info('Question created: id=%s', question.id)

    def perform_destroy(self, instance: Question):
        question_id = int(instance.id)
        answers_count = instance.answers.count()
        instance.delete()
        logger.info('Question deleted: id=%s answers_cascade=%s', question_id, answers_count)


    @action(detail=True, methods=['post'], url_path='answers')
    def create_answer(self, request: Request, pk: Optional[str]=None) -> Response:
        question = self.get_object()
        uid_res = get_or_create_uid(request)
        ser_in = self.get_serializer(data=request.data)
        ser_in.is_valid(raise_exception=True)

        logger.info(
            'Create answer request question_id=%s uid=%s set_cookie=%s', 
            question.id, str(uid_res.uid), uid_res.need_set_cookie
        )

        answer = add_answer(question=question, user_id=uid_res.uid,
                            text=ser_in.validated_data['text'])
        resp = Response(AnswerSerializer(answer).data, status=status.HTTP_201_CREATED)

        if uid_res.need_set_cookie:
            resp.set_cookie(
                key='uid',
                value=str(uid_res.uid),
                max_age=60*60*24*365,
                samesite='Lax',
            )
        return resp


class AnswerRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    queryset = Answer.objects.select_related('question')
    http_method_names = ['get', 'delete']
    serializer_class = AnswerSerializer
