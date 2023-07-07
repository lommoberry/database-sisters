from django.db import models
from django import forms
from django.db import connection

# Create your models here.
class YourForm(forms.ModelForm):
    with connection.cursor as cursor:
        model = "journal"
        fields = '__all__'