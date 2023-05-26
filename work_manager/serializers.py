from django.core.exceptions import ValidationError

from rest_framework import serializers

from work_manager.models import WorkOrder


class WorkOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrder

        fields = [
            "work_order_number",
            "assigned_to",
            "room",
            "finished_at",
            "work_type",
            "work_status",
        ]
        read_only = [
            "work_order_number",
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["created_by"] = request.user
        try:
            return super().create(validated_data)
        except ValidationError as e:
            raise serializers.ValidationError(e.message)
