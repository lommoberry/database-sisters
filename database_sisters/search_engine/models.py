from django.db import models

# jess db test
# sorry that this has taken me genuinely 4 hours to figure out lmao i do not know how to use django at all
class Student(models.Model):
    student_id = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)

    def _str_(self):
        return self.student_id
