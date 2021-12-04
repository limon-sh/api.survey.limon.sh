from django.db import models
from django.db.models import UniqueConstraint
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from libs.models import BaseModel


class Survey(BaseModel):
    """
    Model of the object of the survey.
    """

    name = models.CharField(
        max_length=64, unique=True, verbose_name='Survey name'
    )
    slug = models.SlugField(unique=True)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Category(BaseModel):
    """
    Category model for combining questions into groups.
    """

    title = models.CharField(max_length=64, verbose_name='Category title')
    survey = models.ForeignKey(
        to='survey.Survey', on_delete=models.PROTECT
    )

    class Meta:
        verbose_name_plural = 'Categories'
        constraints = [
            UniqueConstraint(
                name='unique_category', fields=('title', 'survey')
            )
        ]

    def __str__(self) -> str:
        return self.title


class Question(BaseModel):
    """
    Model of the question of the survey.
    """

    class Type(models.TextChoices):
        SINGLE_CHOICE = 'single_choice', _('Single choice')
        MULTIPLE_CHOICE = 'multiple_choice', _('Multiple choice')

    title = models.CharField(max_length=512)
    order = models.PositiveSmallIntegerField()
    type = models.CharField(max_length=32, choices=Type.choices)
    category = models.ForeignKey(
        to='survey.Category', on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return self.title


class Answer(BaseModel):
    """
    Model of the answer of the survey.
    """

    class Type(models.TextChoices):
        CHECKBOX = 'checkbox', _('Checkbox')
        RADIO_BUTTON = 'radio_button', _('Radio button')
        TEXT_INPUT = 'text_input', _('Text input')

    title = models.CharField(max_length=512)
    order = models.PositiveSmallIntegerField()
    type = models.CharField(max_length=32, choices=Type.choices)
    question = models.ForeignKey(
        to='survey.Question', on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return self.title


class Result(BaseModel):
    """
    Model of the result for the question.
    """

    question = models.ForeignKey(
        to='survey.Question', on_delete=models.CASCADE
    )
    answer = models.ForeignKey(
        to='survey.Answer', on_delete=models.CASCADE
    )
    value = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self) -> str:
        return 'Result'
