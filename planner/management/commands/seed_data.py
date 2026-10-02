from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from planner.models import StudyTask, Subject


class Command(BaseCommand):
    help = "Seed sample subjects and tasks for testing and demonstration."

    def handle(self, *args, **kwargs):
        user_model = get_user_model()
        user, created = user_model.objects.get_or_create(username="demo_student", defaults={"email": "demo@example.com"})
        if created:
            user.set_password("demo12345")
            user.save()

        subjects = [
            ("Python", "Core programming concepts and practice."),
            ("Database Management", "SQL queries and database design."),
            ("Web Development", "HTML, CSS, and frontend basics."),
            ("Data Structures", "Algorithms and abstract data structures."),
        ]

        for name, description in subjects:
            subject, _ = Subject.objects.get_or_create(user=user, name=name, defaults={"description": description})
            if subject.description != description:
                subject.description = description
                subject.save()

        sample_tasks = [
            ("Python", "Complete Python basics", "Review loops, functions, and variables.", "HIGH", date.today() + timedelta(days=1), True),
            ("Database Management", "Practice SQL queries", "Write select, join, and filter statements.", "HIGH", date.today() + timedelta(days=3), False),
            ("Web Development", "Create HTML page", "Build a responsive layout using HTML and CSS.", "MEDIUM", date.today() + timedelta(days=6), False),
            ("Data Structures", "Study sorting algorithms", "Review bubble sort and quick sort logic.", "MEDIUM", date.today() + timedelta(days=2), True),
        ]

        for subject_name, title, description, priority, deadline, completed in sample_tasks:
            subject = Subject.objects.get(user=user, name=subject_name)
            StudyTask.objects.get_or_create(
                user=user,
                subject=subject,
                title=title,
                defaults={
                    "description": description,
                    "priority": priority,
                    "deadline": deadline,
                    "completed": completed,
                },
            )

        self.stdout.write(self.style.SUCCESS("Sample study data created successfully."))
