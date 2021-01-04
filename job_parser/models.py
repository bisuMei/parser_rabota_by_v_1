from django.db import models
import datetime
# Create your models here.


class Job(models.Model):
    title = models.CharField(max_length=50)
    company = models.CharField(max_length=50)
    date = models.DateField()
    link = models.URLField(unique=True)

    def __str__(self):
        return self.title
