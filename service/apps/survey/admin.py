from django.contrib import admin
from django.db.models import Count
from django.utils import timezone

from .models import Survey, Category, Question, Result, Answer


class AnswerInlineAdmin(admin.TabularInline):
    model = Answer
    extra = 0


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    list_display = ('name', 'start_at', 'end_at', 'is_active')

    @admin.display(boolean=True)
    def is_active(self, obj) -> bool:
        return obj.start_at <= timezone.now() <= obj.end_at


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_filter = ('survey__name',)
    list_display = ('title', 'questions_count')

    def get_queryset(self, request):
        return Category.objects.select_related(
            'survey'
        ).prefetch_related(
            'question_set'
        ).annotate(
            questions_count=Count('question', distinct=True)
        )

    @staticmethod
    def questions_count(obj) -> int:
        return obj.questions_count


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    ordering = ('order',)
    list_display = ('title', 'order', 'type')
    list_filter = ('category__title', 'category__survey__name')
    inlines = (AnswerInlineAdmin,)

    def get_queryset(self, request):
        return Question.objects.select_related(
            'category',
            'category__survey'
        )


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('question_title', 'answer_title')

    def get_queryset(self, request):
        return Result.objects.select_related(
            'question',
            'answer'
        )

    def has_change_permission(self, request, obj=None) -> bool:
        return False

    @staticmethod
    def question_title(obj) -> str:
        return obj.question.title

    @staticmethod
    def answer_title(obj) -> str:
        return obj.answer.title
