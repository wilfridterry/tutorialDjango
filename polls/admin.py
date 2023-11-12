from django.contrib import admin

from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["text"]}),
        ("Date information", {
            "fields": ["published_at"],
            "classes": ["collapse"]
        })
    ]
    inlines = [ChoiceInline]
    list_display = ["text", "published_at", "was_published_recently"]
    list_filter = ["published_at"]
    search_fields = ["text"]

admin.site.register(Question, QuestionAdmin)
