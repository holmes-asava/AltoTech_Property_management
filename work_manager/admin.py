from work_manager.models import WorkOrder

from django.contrib.admin import AdminSite, TabularInline
from django.contrib import admin, messages


class WorkOrderAdmin(admin.ModelAdmin):
    model = WorkOrder
    fields = [
        field.name for field in WorkOrder._meta.fields if field.name not in ["id"]
    ]
    list_display = fields


admin.site.register(WorkOrder, WorkOrderAdmin)
