from django.core.exceptions import ValidationError

from rest_framework import serializers

from work_manager.models import WorkOrder, TechnicianRequest


class WorkOrderSerializer(serializers.ModelSerializer):
    amenity_request_list = serializers.JSONField(required=False)
    description = serializers.CharField(required=False)
    defect_type = serializers.ChoiceField(
        choices=TechnicianRequest.DefectType.choices, required=False
    )

    class Meta:
        model = WorkOrder

        fields = [
            "work_order_number",
            "assigned_to",
            "room",
            "finished_at",
            "work_type",
            "work_status",
            "amenity_request_list",
            "description",
            "defect_type",
        ]
        read_only = [
            "work_order_number",
        ]

    def validate(self, data):
        amenity_request_list = data.get("amenity_request_list")
        description = data.get("description")
        defect_type = data.get("defect_type")
        work_type = data.get("work_type")
        if amenity_request_list and work_type != WorkOrder.WorkType.AMENITY_REQUEST:
            raise serializers.ValidationError(
                "This WorkOrder type doesn't support amenity_request_list field"
            )
        if description and work_type != WorkOrder.WorkType.MAID_REQUEST:
            raise serializers.ValidationError(
                "This WorkOrder type doesn't support description field"
            )
        if defect_type and work_type != WorkOrder.WorkType.TECHNICIAN_REQUEST:
            raise serializers.ValidationError(
                "This WorkOrder type doesn't support defect_type field"
            )
        return super().validate(data)

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["created_by"] = request.user
        try:
            return super().create(validated_data)
        except ValidationError as e:
            detail = getattr(e, "message", None) or str(e)
            raise serializers.ValidationError(detail)


class UpdateWorkOrderSerializer(WorkOrderSerializer):
    class Meta:
        model = WorkOrder

        fields = [
            "assigned_to",
            "room",
            "finished_at",
            "work_status",
            "amenity_request_list",
            "description",
            "defect_type",
        ]
