from rest_framework import serializers
from to_do_list_api.models import Task


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ["id", "title", "description", "due_date", "status"]

    def validate_status(self, value):
        valid_statuses = dict(Task.STATUS_CHOICES)
        if value not in valid_statuses:
            raise serializers.ValidationError(
                f"Invalid status. Acceptable values: {list(valid_statuses.keys())}"
            )
        return value
