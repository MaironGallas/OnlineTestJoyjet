from django.db import models

# Create your models here.

class Payload(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    articles = models.JSONField()
    carts = models.JSONField()
    delivery_fees = models.JSONField(default=list)
    discounts = models.JSONField(default=list)
