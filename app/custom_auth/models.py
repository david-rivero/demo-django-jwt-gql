from django.db import models
from django.contrib.auth.models import User


class TokenUser(models.Model):
    user = models.ForeignKey(User, on_delete='cascade')
    token = models.TextField()
