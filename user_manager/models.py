import uuid

from django.apps import apps
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.db.models import Max, Q
from django.db.models.constraints import UniqueConstraint
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

from user_manager.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    class RoleType(models.IntegerChoices):
        GUEST = 0
        MAID = 1
        SUPERVISOR = 2

    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        "email address", unique=True, default=None, blank=True, null=True
    )
    first_name = models.CharField("first name", max_length=32, blank=True)
    last_name = models.CharField("last name", max_length=32, blank=True)
    role_type = models.IntegerField(choices=RoleType.choices, default=RoleType.GUEST)
    is_staff = models.BooleanField("staff status", default=False)
    USERNAME_FIELD = "email"
    objects = UserManager()

    @property
    def is_maid(self):
        return self.role_type == self.RoleType.MAID

    @property
    def is_supervisor(self):
        return self.role_type == self.RoleType.SUPERVISOR

    @property
    def is_guest(self):
        return self.role_type == self.RoleType.SUPERVISOR
