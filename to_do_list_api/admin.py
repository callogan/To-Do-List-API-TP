from django.contrib import admin
from to_do_list_api.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "status", "due_date")
    list_filter = ("status", "due_date")
    search_fields = ("title", "description")
    readonly_fields = ("id",)
    fieldsets = (
        ("Main information", {
            "fields": ("id", "title", "description")
        }),
        ("Status and time", {
            "fields": ("status", "due_date")
        }),
    )


admin.site.register(Task, TaskAdmin)

