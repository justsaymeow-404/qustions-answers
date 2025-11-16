import logging
from uuid import UUID

from django.db import transaction

from questions.models import Answer, Question


logger = logging.getLogger('questions')


@transaction.atomic
def add_answer(*, question: Question, user_id: UUID, text: str) -> Answer:
    answer = Answer.objects.create(
        question=question,
        user_id=user_id,
        text=text
    )
    logger.info(
        'Answer created: id=%s question_id=%s, user_id=%s', answer.id, question.id, str(user_id)
    )
    return answer
