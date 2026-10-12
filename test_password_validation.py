import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "studymate.settings")
django.setup()

from django.contrib.auth import password_validation
from django import forms
from django.core.exceptions import ValidationError as CoreVE

print("forms.ValidationError is subclass of CoreVE:", issubclass(forms.ValidationError, CoreVE))

try:
    password_validation.validate_password("12345")
except CoreVE as e:
    print("Caught as CoreVE:", type(e).__name__, "-", e.messages)
except forms.ValidationError as e:
    print("Caught as forms.ValidationError")
except Exception as e:
    print("Caught as generic:", type(e).__name__)
