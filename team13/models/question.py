from django.db import models

from team13.models import base_models


class Question(base_models.TimeModel, base_models.HistoricalModel):
    """Assessment questions and their exemplar responses."""
    QUESTION_TYPES = [
        ('writing', 'Writing'),
        ('speaking', 'Speaking'),
    ]
    title = models.CharField(max_length=255)
    text = models.TextField()
    sample_correct_answer = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, db_index=True)
