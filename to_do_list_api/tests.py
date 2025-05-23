from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from to_do_list_api.models import Task


class TaskAuthenticationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword"
        )
        self.admin_user = User.objects.create_user(
            username="adminuser",
            email="admin@example.com",
            password="adminpassword",
            is_staff=True
        )

        self.task = Task.objects.create(
            title="Test Task",
            description="Test Description",
            status="P"
        )

        self.tasks_url = reverse("tasks:task-list")
        self.task_detail_url = reverse(
            "tasks:task-detail",
            kwargs={"pk": self.task.pk}
        )

        self.client = APIClient()
        self.user_client = APIClient()
        self.admin_client = APIClient()
        self.client.throttle_classes = []

        user_refresh = RefreshToken.for_user(self.user)
        admin_refresh = RefreshToken.for_user(self.admin_user)

        self.user_client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {user_refresh.access_token}"
        )
        self.admin_client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {admin_refresh.access_token}"
        )

    def test_unauthenticated_user_can_read(self):
        response = self.client.get(self.tasks_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(self.task_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_user_cannot_write(self):
        task_data = {
            "title": "New Task",
            "description": "New Description",
            "status": "P"
        }
        response = self.client.post(self.tasks_url, task_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.put(
            self.task_detail_url,
            {"title": "Updated Task", "status": "P"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.delete(self.task_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_create_task(self):
        task_data = {
            "title": "User Task",
            "description": "User Description",
            "status": "P"
        }
        response = self.user_client.post(self.tasks_url, task_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)

    def test_authenticated_user_can_modify_any_task(self):
        response = self.user_client.put(
            self.task_detail_url,
            {"title": "Modified Task", "status": "P"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Modified Task")

    def test_admin_can_modify_any_task(self):
        response = self.admin_client.put(
            self.task_detail_url,
            {"title": "Admin Modified Task", "status": "P"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Admin Modified Task")


class TaskAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword"
        )

        self.pending_task = Task.objects.create(
            title="Pending Task",
            description="Task in pending status",
            status="P"
        )
        self.in_progress_task = Task.objects.create(
            title="In Progress Task",
            description="Task in progress",
            status="IP"
        )
        self.completed_task = Task.objects.create(
            title="Completed Task",
            description="Task is completed",
            status="C"
        )

        self.tasks_url = reverse("tasks:task-list")

        self.client = APIClient()
        user_refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {user_refresh.access_token}"
        )

    def test_get_task_list(self):
        response = self.client.get(self.tasks_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 3)

    def test_filter_tasks_by_status(self):
        response = self.client.get(f"{self.tasks_url}?status=IP")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(
            response.data["results"][0]["title"], "In Progress Task"
        )

        response = self.client.get(f"{self.tasks_url}?status=C")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(
            response.data["results"][0]["title"], "Completed Task"
        )

    def test_create_task_with_invalid_status(self):
        task_data = {
            "title": "Invalid Status Task",
            "description": "This task has an invalid status",
            "status": "X"
        }
        response = self.client.post(self.tasks_url, task_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("status", response.data)

    def test_update_task_status(self):
        task_detail_url = reverse(
            "tasks:task-detail",
            kwargs={"pk": self.pending_task.pk}
        )
        response = self.client.patch(
            task_detail_url,
            {"status": "C"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.pending_task.refresh_from_db()
        self.assertEqual(self.pending_task.status, "C")

    def test_delete_task(self):
        admin_user = User.objects.create_user(
            username="adminuser",
            email="admin@example.com",
            password="adminpassword",
            is_staff=True
        )
        admin_client = APIClient()
        admin_refresh = RefreshToken.for_user(admin_user)
        admin_client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {admin_refresh.access_token}"
        )

        task_detail_url = reverse(
            "tasks:task-detail",
            kwargs={"pk": self.completed_task.pk}
        )
        response = admin_client.delete(task_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 2)
