from django.db import models

'''
project databases

TODO:
- add constraints/foreign keys to all tables [pk, fk, autoincrement, delete cascade, not null, etc.]
- correct max_length for models.CharField
- create associative tables: AUTHOR_JOURNAL, JOURNAL_COUNTRY, SITE_ENTRY
- populate tables with correct data (tables populated with sample data (via shell) for now)
- figure out how to actually store an image via BlobField lmao

# view tables: https://inloop.github.io/sqlite-viewer/ then drag and drop db.sqlite3
'''


class JOURNAL(models.Model):
    # need to fix auto id attrib (for all tables)
    JOURNAL_ID = models.IntegerField()
    JOURNAL_NUM_ENTRIES = models.IntegerField()
    JOURNAL_CENTURY = models.IntegerField()
    JOURNAL_TITLE = models.CharField(max_length=200)  # fix max length for all charfields later


class COUNTRY(models.Model):
    COUNTRY_ID = models.IntegerField()
    COUNTRY_NAME = models.CharField(max_length=200)


class JOURNAL_ENTRY(models.Model):
    ENTRY_ID = models.IntegerField()
    ENTRY_TEXT = models.CharField(max_length=1000)


class SITE(models.Model):
    SITE_ID = models.IntegerField()
    SITE_NAME = models.CharField(max_length=200)


class SKETCH(models.Model):
    SKETCH_ID = models.IntegerField()
    # SKETCH = models.BlobField()


class DATE(models.Model):
    DATE_FULL = models.IntegerField()
    MONTH = models.IntegerField()
    DAY = models.IntegerField()
    YEAR = models.IntegerField()


class AUTHOR(models.Model):
    AUTH_ID = models.IntegerField()
    AUTH_FNAME = models.CharField(max_length=200)
    AUTH_LNAME = models.CharField(max_length=200)

