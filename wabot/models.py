from django.db import models


class MessageWABot(models.Model):
    customer = models.CharField(max_length=15)
    from_phone = models.CharField(max_length=15)
    to_phone = models.CharField(max_length=15)
    message = models.CharField(max_length=500)
    request_at = models.DateTimeField()

    def __str__(self):
        return self.customer
