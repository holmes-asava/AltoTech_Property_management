from rest_framework import generics, mixins, serializers, status, viewsets
from rest_framework.decorators import action, authentication_classes
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from work_manager.models import WorkOrder
from work_manager.serializers import WorkOrderSerializer


class WorkViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer
