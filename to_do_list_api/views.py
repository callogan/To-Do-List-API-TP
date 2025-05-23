from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from to_do_list_api.models import Task
from to_do_list_api.permissions import IsAuthenticatedForWriteOperations
from to_do_list_api.serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    authentication_classes = (JWTAuthentication,)
    queryset = Task.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status", "due_date"]
    permission_classes = [IsAuthenticatedForWriteOperations]
