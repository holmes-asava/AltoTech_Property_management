"""
URL configuration for altoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.contrib import admin
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers
from work_manager.views import WorkViewSet

router = routers.DefaultRouter()
router.register(r"work_order", WorkViewSet, basename="work_order")

schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version="v1",
        description="API for application ",
    ),
)
urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("", include((router.urls, "api"), namespace="v1")),
]
