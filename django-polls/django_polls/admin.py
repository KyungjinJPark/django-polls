from django.contrib import admin

# Register your models here.
from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    list_display = ["question_text", "pub_date", "was_published_recently"]
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"]})
    ]
    inlines = [ChoiceInline]
    search_fields = ["question_text"]
    list_filter = ["pub_date"]

admin.site.register(Question, QuestionAdmin)