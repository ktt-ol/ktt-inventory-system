import os
import os.path

DEBUG = False

SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")

_origin = os.environ.get("CSRF_TRUSTED_ORIGIN", "")
CSRF_TRUSTED_ORIGINS = [_origin] if _origin else []

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.environ.get(
            "DATABASE_PATH", "/data/inventar.db"
        ),
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

TIME_ZONE = "Europe/Berlin"
LANGUAGE_CODE = "de"
SITE_ID = 1
USE_I18N = True
USE_TZ = True

LOCALE_PATHS = [os.environ.get("LOCALE_PATH", "/locale")]

from django.utils.translation import gettext_lazy

LANGUAGES = (
    ("de", gettext_lazy("German")),
    ("en", gettext_lazy("English")),
)

MEDIA_ROOT = os.environ.get("MEDIA_ROOT", "/data/uploaded/")
MEDIA_URL = "/uploaded/"

STATIC_ROOT = os.environ.get("STATIC_ROOT", "/static/")
STATIC_URL = "/static/"

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

MIDDLEWARE = (
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.locale.LocaleMiddleware",
)

ROOT_URLCONF = "inventar.urls"
WSGI_APPLICATION = "inventar.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(os.path.dirname(__file__), "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "inventory.context_processors.barcode_settings",
            ],
        },
    },
]

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "inventory",
)

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}

FORCE_SCRIPT_NAME = ""
LOGIN_REDIRECT_URL = "/"
