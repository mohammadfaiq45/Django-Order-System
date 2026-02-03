import uuid
from django.db import models

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField()
    visibility = models.BooleanField(default=True)
    available_units = models.PositiveIntegerField()

    def __str__(self):
        return self.name

