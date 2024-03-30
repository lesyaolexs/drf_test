from django.db import transaction

from app.models import Group, User
from drf_test.celery import app


@app.task()
@transaction.atomic
def clean_db():
    User.objects.all().delete()
    Group.objects.all().delete()
