from datetime import datetime as dt

import graphene
from graphene_django.types import DjangoObjectType

from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from .models import TokenUser


class UserType(DjangoObjectType):
    class Meta:
        model = User


class LoginQuery(object):
    login = graphene.Field(UserType)
    logout = graphene.Field(UserType)

    def create_token(self, login_obj):
        password_obj = {'password': login_obj.password}
        key = dt.now().strftime('%Y-%M-%dT%H:%M:%SZ')
        token = jwt.encode(
            password_obj, key,
            algorithm=settings.DEFAULT_ALGORITHM)
        TokenUser.objects.create(user=user, token=token)

    def resolve_login(self, info):
        login_obj = info.context.login_obj
        user = User.objects.get(email=login_obj.email)

        if not user:
            return None
        else:
            try:
                validate_password(login_obj.password, user=user)
            except ValidationError:
                return None

        self.create_token(login_obj)
        return user


schema = graphene.Schema(query=LoginQuery)
