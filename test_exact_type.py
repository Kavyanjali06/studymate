import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "studymate.settings")
django.setup()

from django.contrib.auth import password_validation
from django import forms
from django.core.exceptions import ValidationError as CoreVE

try:
    password_validation.validate_password("12345")
except Exception as e:
    print("Exact type:", type(e))
    print("type(e) is forms.ValidationError:", type(e) is forms.ValidationError)
    print("type(e) is CoreVE:", type(e) is CoreVE)
    print("isinstance forms.ValidationError:", isinstance(e, forms.ValidationError))
    print("isinstance CoreVE:", isinstance(e, CoreVE))
