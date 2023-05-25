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
from user_manager.models import User


class WorkOrderManager(models.Manager):
    def create(self, *args, **kwargs):
        if str(self) == "work_manager.WorkOrder.objects":
            type = kwargs.get("work_type")
            if type == None:
                raise ValidationError("work_type can't be None")
            TypeModel = apps.get_model(
                "work_manager", WorkOrder.WorkType(type).label.replace(" ", "")
            )
            return TypeModel.objects.create(*args, **kwargs)
        return super(WorkOrderManager, self).create(*args, **kwargs)


class WorkOrder(models.Model):
    objects = WorkOrderManager()

    class WorkType(models.IntegerChoices):
        CLEANING = 0, "Cleaning"
        MAID_REQUEST = 1, "Maid Request"
        TECHNICIAN_REQUEST = 2, "Technician Request"
        AMENITY_REQUEST = 3, "Amenity Request"

    class WorkStatus(models.IntegerChoices):
        CREATED = 0, "Created"
        ASSIGNED = 1, "Assigned"
        IN_PROGRESS = 2, "In Progress"
        DONE = 3, "Done"
        CANCEL = 4, "Cancel"
        CANCEL_BY_GUEST = 5, "Cancel by guest"

    work_order_nuber = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=None,
        related_name="created_work",
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        related_name="assigned_task",
    )
    room = models.IntegerField()
    start_at = models.DateTimeField(editable=False, auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True, default=None)
    work_type = models.IntegerField(choices=WorkType.choices, default=WorkType.CLEANING)
    work_status = models.IntegerField(
        choices=WorkStatus.choices, default=WorkStatus.CREATED
    )

    def clean(self):
        if (
            self.work_status == self.WorkStatus.CANCEL_BY_GUEST
            and self.work_type != self.WorkType.CLEANING
        ):
            raise ValidationError(
                f"Work type doesn't suppose this status({self.WorkStatus.CANCEL_BY_GUEST.label})"
            )
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Cleaning(WorkOrder):
    def save(self, *args, **kwargs):
        self.work_type = self.WorkType.CLEANING
        super().save(**kwargs)


class MaidRequest(WorkOrder):
    description = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.work_type = self.WorkType.MAID_REQUEST
        super().save(**kwargs)


class TechnicianRequest(WorkOrder):
    class DefectType(models.IntegerChoices):
        Electricity = 0, "Electricity"
        AC = 1, "AC"
        PLUMBING = 2, "Plumbing"
        INTERNET = 3, "Internet"

    defect_type = models.IntegerField(choices=DefectType.choices)

    def save(self, *args, **kwargs):
        self.work_type = self.WorkType.TECHNICIAN_REQUEST
        super().save(**kwargs)


class AmenityRequest(WorkOrder):
    amenity_request_list = models.JSONField()

    def save(self, *args, **kwargs):
        self.work_type = self.WorkType.AMENITY_REQUEST
        super().save(**kwargs)
