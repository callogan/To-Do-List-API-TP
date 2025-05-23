from django.urls import path, include
from rest_framework.routers import DefaultRouter

from to_do_list_api.views import TaskViewSet

app_name = "to_do_list_api"

router = DefaultRouter()

router.register("to_do_list_api", TaskViewSet, basename="to-do-list-api")

urlpatterns = [
    path("", include(router.urls)),
]
