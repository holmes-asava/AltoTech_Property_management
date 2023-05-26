from user_manager.models import User
from django.contrib import admin, messages
from django.contrib.admin import AdminSite, TabularInline


class UserAdmin(admin.ModelAdmin):
    model = User
    fields = [
        field.name
        for field in User._meta.fields
        if field.name not in ["id", "password"]
    ]
    search_fields = ["email", "first_name", "last_name"]
    list_display = fields
    list_filter = ["is_superuser", "is_staff"]


admin.site.register(User, UserAdmin)
