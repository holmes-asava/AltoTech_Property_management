"""
Django settings for altotech server project.

Using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Application definition

INSTALLED_APPS = [
    "corsheaders",  # required
    "config",  # above admin for overriding default admin
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "rest_framework",
    "rest_framework.authtoken",
    "drf_yasg",
    "health_check",  # required
    "health_check.db",  # stock Django health checkers
    "health_check.cache",
    "health_check.storage",
    "timezone_field",
    "user_manager",
    "work_manager",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",  # Django basic Auth
)

# LinkedIn general settings

# Custom basic Auth model
AUTH_USER_MODEL = "user_manager.User"

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Setting LOGIN/LOGOUT urls, by default it uses django default login/logout.
# Swagger Login/Logout rely on this setting.
LOGIN_URL = "rest_framework:login"
LOGIN_REDIRECT_URL = "/"
LOGOUT_URL = "rest_framework:logout"
LOGOUT_REDIRECT_URL = "/"
JSON_EDITOR = True

# Rest framework settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "throttling_cache_table",
    }
}

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = "static"
MEDIE_URL = "/media/"
MEDIE_ROOT = "media"

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Django reset password settings
DJANGO_REST_MULTITOKENAUTH_RESET_TOKEN_EXPIRY_TIME = 480  # hours
PASSWORDLESS_TOKEN_EXPIRY_TIME = 120  # minutes
DJANGO_REST_PASSWORDRESET_NO_INFORMATION_LEAKAGE = (
    True  # always 200 even if email isn't found in database
)

API_SUBDOMAIN = "api"  # used for the API subdomain
EVENT_ADMIN_SUBDOMAIN = "app"  # used for checking if request from event admin
DECIMAL_PLACE_FOR_ROUNDING = 2
DEFAULT_REGISTER_TOPUP_AMOUNT = 0
