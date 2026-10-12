import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "studymate.settings")
django.setup()

from django.contrib.auth import password_validation
from django import forms

try:
    password_validation.validate_password("12345")
except forms.ValidationError as e:
    print("CAUGHT by forms.ValidationError")
except Exception as e:
    print("NOT CAUGHT by forms.ValidationError - type:", type(e).__name__)
