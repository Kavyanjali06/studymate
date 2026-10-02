from django.contrib import admin

from .models import StudyTask, Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "created_at")
    list_filter = ("user",)
    search_fields = ("name", "description")
    ordering = ("-created_at",)


@admin.register(StudyTask)
class StudyTaskAdmin(admin.ModelAdmin):
    list_display = ("title", "subject", "user", "priority", "deadline", "completed")
    list_filter = ("priority", "completed", "subject", "user")
    search_fields = ("title", "description")
    ordering = ("-deadline",)
