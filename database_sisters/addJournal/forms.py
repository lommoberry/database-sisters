from django import forms
from django.db import connection

# Create your forms here.
class YourForm(forms.ModelForm):
    with connection.cursor as cursor:
        model = "journal"
        fields = '__all__'

