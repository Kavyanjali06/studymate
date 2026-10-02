from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import StudyTask, Subject


class StudyMateTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="student",
            email="student@example.com",
            password="StrongPass123",
        )
        self.client.login(username="student", password="StrongPass123")
        self.subject = Subject.objects.create(user=self.user, name="Python", description="Programming concepts")

    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "StudyMate")

    def test_user_registration(self):
        self.client.logout()
        response = self.client.post(
            reverse("register"),
            {
                "username": "newstudent",
                "email": "newstudent@example.com",
                "password": "StrongPass123",
                "confirm_password": "StrongPass123",
            },
        )
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(get_user_model().objects.filter(username="newstudent").exists())

    def test_login_redirects_to_dashboard(self):
        self.client.logout()
        response = self.client.post(
            reverse("login"),
            {"username": "student", "password": "StrongPass123"},
            follow=True,
        )
        self.assertRedirects(response, reverse("dashboard"))

    def test_dashboard_requires_authentication(self):
        self.client.logout()
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_subject_creation(self):
        response = self.client.post(
            reverse("subject_add"),
            {"name": "Database", "description": "SQL practice"},
        )
        self.assertRedirects(response, reverse("subjects"))
        self.assertTrue(Subject.objects.filter(user=self.user, name="Database").exists())

    def test_subject_editing(self):
        response = self.client.post(
            reverse("subject_edit", args=[self.subject.pk]),
            {"name": "Updated Python", "description": "Updated description"},
        )
        self.assertRedirects(response, reverse("subjects"))
        self.subject.refresh_from_db()
        self.assertEqual(self.subject.name, "Updated Python")

    def test_subject_deletion(self):
        response = self.client.get(reverse("subject_delete", args=[self.subject.pk]))
        self.assertRedirects(response, reverse("subjects"))
        self.assertFalse(Subject.objects.filter(pk=self.subject.pk).exists())

    def test_task_creation(self):
        response = self.client.post(
            reverse("task_add"),
            {
                "subject": self.subject.pk,
                "title": "Complete assignment",
                "description": "Finish lab tasks.",
                "priority": "HIGH",
                "deadline": "2030-12-15",
            },
        )
        self.assertRedirects(response, reverse("tasks"))
        self.assertTrue(StudyTask.objects.filter(user=self.user, title="Complete assignment").exists())

    def test_task_completion_and_deletion(self):
        task = StudyTask.objects.create(
            user=self.user,
            subject=self.subject,
            title="Read chapter",
            description="Prepare notes",
            priority="MEDIUM",
            deadline="2030-10-10",
        )

        response = self.client.get(reverse("task_complete", args=[task.pk]))
        self.assertRedirects(response, reverse("tasks"))
        task.refresh_from_db()
        self.assertTrue(task.completed)

        response = self.client.get(reverse("task_delete", args=[task.pk]))
        self.assertRedirects(response, reverse("tasks"))
        self.assertFalse(StudyTask.objects.filter(pk=task.pk).exists())

    def test_user_isolation_prevents_access(self):
        other_user = get_user_model().objects.create_user(
            username="otherstudent",
            email="otherstudent@example.com",
            password="StrongPass123",
        )
        other_subject = Subject.objects.create(user=other_user, name="Chemistry", description="Lab work")

        response = self.client.get(reverse("subject_edit", args=[other_subject.pk]))
        self.assertEqual(response.status_code, 404)
