import re
import sys


from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from django.db import IntegrityError
from django.db.models import Q

from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from work_manager.models import WorkOrder


class WorkOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrder
        fields = "__all__"
