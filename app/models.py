import uuid

from django.core.exceptions import ValidationError
from django.db import models


def validate_login(login: str) -> str:
    """
    Check that the login starts with a letter
    :return:
    """
    if not login or not login[0].isalpha():
        raise ValidationError(" Login must starts with a letter")
    return login


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

    id = models.UUIDField(
        primary_key=True, auto_created=True, default=uuid.uuid4, editable=False
    )
    login = models.CharField(
        unique=True, max_length=16, validators=[validate_login], null=False
    )
    sex = models.CharField(choices=SEX_CHOICES, max_length=6, null=False)
    birth_date = models.DateField()

    def __str__(self) -> str:
        return self.id
