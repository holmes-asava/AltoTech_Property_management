# import re

# from config.settings.base import BASE_DIR
# from django.contrib import admin, messages
# from django.contrib.admin import AdminSite, TabularInline
# from django.contrib.auth.forms import AuthenticationForm
# from django.core.exceptions import ValidationError
# from django.db import models
# from django.db.models import Q
# from django.forms import BaseInlineFormSet, Textarea
# from django.utils.translation import gettext_lazy as _
# from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
# from import_export.admin import ImportExportMixin

# __all__ = [
#     "admin_site",
#     "CustomBaseAdmin",
#     "CustomTabularInline",
#     "CustomPresentationDocumentTabularInline",
#     "CalculatedBooleanFilter",
# ]


# class CustomAdminAuthenticationForm(AuthenticationForm):
#     error_messages = {
#         **AuthenticationForm.error_messages,
#         "invalid_login": _(
#             "Please enter the correct %(username)s and password for a SUPERUSER or STAFF account. "
#             "Note that both fields may be case-sensitive."
#         ),
#     }
#     required_css_class = "required"

#     def confirm_login_allowed(self, user):
#         super().confirm_login_allowed(user)
#         if not (user.is_superuser or user.is_staff):
#             raise ValidationError(
#                 self.error_messages["invalid_login"],
#                 code="invalid_login",
#                 params={"username": self.username_field.verbose_name},
#             )


# class CustomAdminSite(AdminSite):
#     login_form = CustomAdminAuthenticationForm

#     def has_permission(self, request):
#         return bool(
#             request.user.is_active
#             and (request.user.is_superuser or request.user.is_staff)
#         )


# class CustomTabularInline(TabularInline):
#     extra = 1
#     formfield_overrides = {
#         models.TextField: {"widget": Textarea(attrs={"rows": 4, "cols": 40})},
#     }
#     classes = ("collapse",)


# BREAKS_AUTOCOMPLETE_FIELDS = [
#     "auth_form_details",
#     "dropdown_specify_options",
#     "dropdown_options",
#     "details",
#     "socials",
# ]


# def order_ticket(queryset):
#     return queryset.order_by("info__event__name", "info__name")


# class CustomBaseAdmin(ImportExportMixin, DynamicArrayMixin, admin.ModelAdmin):
#     """
#     Notes:
#         change_list_template = None
#             if the template path is equal to default change list path of Django admin
#             otherwise the path will be equal to 'admin/import_export/change_list_import_export.html'
#     """

#     ordering = ("id",)

#     formfield_overrides = {
#         models.TextField: {"widget": Textarea(attrs={"rows": 4, "cols": 40})},
#     }

#     def __init__(self, model, admin_site):
#         super().__init__(model, admin_site)
#         if self.list_display == ("__str__",):
#             self.list_display = [field.name for field in self.opts.fields]

#         all_field_names = [field.name for field in self.opts.fields]

#         can_use_autocomplete = True
#         for f in BREAKS_AUTOCOMPLETE_FIELDS:
#             if f in all_field_names:
#                 can_use_autocomplete = False
#                 break

#         if can_use_autocomplete:
#             if "organization" in all_field_names:
#                 self.autocomplete_fields += ("organization",)
#             if "event" in all_field_names:
#                 self.autocomplete_fields += ("event",)
#             if "stage" in all_field_names:
#                 self.autocomplete_fields += ("stage",)
#             if "landing_page" in all_field_names:
#                 self.autocomplete_fields += ("landing_page",)
#             if "asset" in all_field_names:
#                 self.autocomplete_fields += ("asset",)

#     def save_model(self, request, obj, form, change):
#         try:
#             super().save_model(request, obj, form, change)
#         except Exception as e:
#             self.message_user(request, e, level=messages.ERROR)


# admin_site = CustomAdminSite()
