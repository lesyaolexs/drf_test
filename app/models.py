import uuid

from django.core.exceptions import ValidationError
from django.db import models


def validate_login(login: str) -> str:
    """
    Check that the login starts with a letter and is alphanumeric
    :return:
    """
    if not login or not login.isalnum() or not login[0].isalpha():
        raise ValidationError("Login should start with a letter and be alphanumeric")
    return login


class Group(models.Model):
    id = models.UUIDField(
        primary_key=True, auto_created=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField(
        unique=True, max_length=16, validators=[validate_login], null=False
    )
    public = models.BooleanField(null=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.id


class User(models.Model):
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
    groups = models.ManyToManyField(Group)

    class Meta:
        ordering = ["login"]

    def __str__(self) -> str:
        return self.id
