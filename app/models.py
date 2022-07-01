import uuid

from django.db import models


class CustomUser(models.Model):
    SEX_CHOICES = (
        (
            "male",
            "Male",
        ),
        (
            "female",
            "Female",
        ),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4())
    login = models.CharField(unique=True, max_length=16)
    sex = models.CharField(choices=SEX_CHOICES, max_length=6)
    birth_date = models.DateTimeField()
