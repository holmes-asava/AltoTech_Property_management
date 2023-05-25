import os

from .base import *

ENVIRONMENT = "dev"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "whatever-secret-key"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ORIGIN_DOMAIN = "localhost"
ALLOWED_HOSTS = ["*"]
CORS_ORIGIN_ALLOW_ALL = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "DEBUG"),
            "propagate": False,
        },
    },
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "password",
        "HOST": "db",
        "PORT": "5432",
    }
}

SUPER_ADMIN_PASS = "test_password"
