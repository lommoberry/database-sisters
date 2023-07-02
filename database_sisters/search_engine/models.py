from django.db import models

# # jess db test
# # sorry that this has taken me genuinely 4 hours to figure out lmao i do not know how to use django at all
# class Student(models.Model):
#     student_id = models.CharField(max_length=200)
#     firstname = models.CharField(max_length=200)
#     lastname = models.CharField(max_length=200)
#
#     def _str_(self):
#         return self.student_id

# project databases
# initially created w/o constraints/foreign keys - will add in later
# tables populated with sample data (via shell) for now
# view tables: https://inloop.github.io/sqlite-viewer/ then drag and drop db.sqlite3


class JOURNAL(models.Model):
    # need to fix auto id attrib (for all tables)
    JOURNAL_ID = models.IntegerField()
    JOURNAL_NUM_ENTRIES = models.IntegerField()
    JOURNAL_CENTURY = models.IntegerField()
    JOURNAL_TITLE = models.CharField(max_length=200)  # fix max length for all charfields later


class AUTHOR(models.Model):
    AUTH_ID = models.IntegerField()
    AUTH_FNAME = models.CharField(max_length=200)
    AUTH_LNAME = models.CharField(max_length=200)


