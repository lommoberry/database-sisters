from django.db import models

# Create your models here.
class Journal(models.Model):
    Journal_Title = models.CharField(max_length=100)
    Num_Entries = models.IntegerField()
    Century = models.CharField(max_length=2) #ex.) 19
    Journal_ID = models.IntegerField(primary_key=True)

