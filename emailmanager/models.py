from django.db import models

class Message(models.Model):
    title = models.CharField()
    date_sent = models.DateTimeField()
    date_received = models.DateTimeField()
    desription = models.CharField()
    files_enclosed = models.CharField()
