from rest_framework import generics, mixins, viewsets
from rest_framework.decorators import action, authentication_classes
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from config.permissions import *
from work_manager.models import WorkOrder
from work_manager.serializers import WorkOrderSerializer, UpdateWorkOrderSerializer


class WorkViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
    mixins.UpdateModelMixin,
):
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer

    def get_permissions(self):
        permission_classes = None
        if self.action in ["partial_update", "update"]:
            permission_classes = [IsMaid | IsSupervisor]
        elif self.action in ["create"]:
            permission_classes = [IsAuthenticated]

        return [
            permission()
            for permission in (permission_classes or self.permission_classes)
        ]

    def get_queryset(self):
        if self.request.user.is_guest:
            return self.queryset.filter(created_by=self.request.user)
        return self.queryset

    def get_serializer_class(self):
        if self.action in ["partial_update", "update"]:
            return UpdateWorkOrderSerializer

        return self.serializer_class
