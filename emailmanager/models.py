from django.db import models

class Message(models.Model):
    message_id=models.CharField()
    from_msg = models.CharField()
    to_msg = models.CharField()
    date_sent = models.DateTimeField()
    date_received = models.DateTimeField()
    subject = models.CharField()
    files_enclosed = models.CharField()
