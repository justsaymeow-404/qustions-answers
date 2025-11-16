from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import QuestionViewSet, AnswerRetrieveDestroyAPIView

app = 'questions'

router = DefaultRouter()
router.register(r'questions', QuestionViewSet, basename='questions')

urlpatterns = [
    path('', include(router.urls)),
    path('answers/<int:pk>/', AnswerRetrieveDestroyAPIView.as_view(), name='answer-detail'),
]
