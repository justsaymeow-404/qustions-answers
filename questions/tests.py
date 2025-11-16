from uuid import uuid4

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from questions.models import Answer, Question


API = '/api/v1'


class TestQuestionAPI(APITestCase):
    def test_list_questions_empty(self) -> None:
        result = self.client.get(f'{API}/questions/')
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data['count'], 0)
        self.assertEqual(result.data['results'], [])

    def test_create_and_list_question(self) -> None:
        create_url = f'{API}/questions/'
        result = self.client.post(create_url, data={'text': 'TEST1'}, format='json')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        question_id = result.data['id']

        list_result = self.client.get(create_url)
        self.assertEqual(list_result.status_code, status.HTTP_200_OK)
        self.assertEqual(list_result.data['count'], 1)
        self.assertEqual(list_result.data['results'][0]['id'], question_id)

    def test_answer_retrieve_and_delete(self) -> None:
        question = Question.objects.create(text='TEST2')
        result = self.client.post(f'{API}/questions/{question.id}/answers/',
                                  data={'text': 'TEST_ANSWER2'}, format='json')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        answer_id = result.data['id']

        get_result = self.client.get(f'{API}/answers/{answer_id}/')
        self.assertEqual(get_result.status_code, status.HTTP_200_OK)

        del_result = self.client.delete(f'{API}/answers/{answer_id}/')
        self.assertEqual(del_result.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Answer.objects.filter(id=answer_id).exists())

    def test_delete_question_cascade(self) -> None:
        question = Question.objects.create(text='TEST3')
        url = f'{API}/questions/{question.id}/answers/'
        self.client.post(url, data={'text': 'TEST1'}, format='json')
        self.client.post(url, data={'text': 'TEST2'}, format='json')
        self.assertEqual(Answer.objects.filter(question=question).count(), 2)

        del_question = self.client.delete(f'{API}/questions/{question.id}/')
        self.assertEqual(del_question.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Answer.objects.filter(question=question).count(), 0)

    def test_create_answer_for_nonexistent_question_404(self) -> None:
        result = self.client.post(f'{API}/questions/9999999/answers/',
                                  data={'text': 'TEST_ANSWER'}, format='json')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)
