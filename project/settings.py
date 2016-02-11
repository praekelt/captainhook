import os
import sys

from django.core.urlresolvers import reverse_lazy
from collections import OrderedDict


# Paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def abspath(*args):
    """
    Convert relative paths to absolute paths relative to PROJECT_ROOT
    """
    return os.path.join(PROJECT_ROOT, *args)

PROJECT_MODULE = "captainhook"

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# For Postgres (not location aware) do from command line
# echo "CREATE USER mothership WITH PASSWORD 'mothership'" | sudo -u postgres psql
# echo "CREATE DATABASE mothership WITH OWNER mothership ENCODING 'UTF8'" | sudo -u postgres psql

# For Postgres (location aware) do from command line
# echo "CREATE USER mothership WITH PASSWORD 'mothership'" | sudo -u postgres psql
# echo "CREATE DATABASE mothership WITH OWNER mothership ENCODING 'UTF8'" | sudo -u postgres psql
# echo "CREATE EXTENSION postgis" | sudo -u postgres psql mothership
# echo "CREATE EXTENSION postgis_topology" | sudo -u postgres psql mothership

# For MySQL remember to first do from a MySQL shell:
# CREATE database mothership;
# GRANT ALL ON mothership.* TO "mothership"@"localhost" IDENTIFIED BY "mothership";
# FLUSH PRIVILEGES;

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "captainhook.db", # Or path to database file if using sqlite3.
        "USER": "captainhook", # Not used with sqlite3.
        "PASSWORD": "captainhook", # Not used with sqlite3.
        "HOST": "", # Set to empty string for localhost. Not used with sqlite3.
        "PORT": "", # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "UTC"
USE_TZ = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = abspath("media")


# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = "/media/"

STATIC_ROOT = abspath("static")

STATIC_URL = "/static/"

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
ADMIN_MEDIA_PREFIX = "/static/admin/"

# Make this unique, and don"t share it with anybody.
SECRET_KEY = "90fa5389da32fb9128404663e6b6ec5327666b4d345e0c12cc429db1"

MIDDLEWARE_CLASSES = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.contrib.flatpages.middleware.FlatpageFallbackMiddleware"
)

# A tuple of callables that are used to populate the context in RequestContext.
# These callables take a request object as their argument and return a
# dictionary of items to be merged into the context.
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
)

ROOT_URLCONF = "project.urls"

INSTALLED_APPS = (
    "captainhook",

    "south",

    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.humanize",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "django.contrib.messages",

    "djcelery",
    "raven.contrib.django",
    "raven.contrib.django.celery",
)

LOGIN_URL = "/login"

LOGIN_REDIRECT_URL = "/"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        }
    },
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "WARN",
            "class": "logging.StreamHandler",
            "formatter": "verbose"
        },
        "sentry": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "raven.contrib.django.handlers.SentryHandler",
        },
    },
    "loggers": {
        "raven": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": True,
        },
        "sentry.errors": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": True,
        },
        "django": {
            "handlers": ["console"],
            "level": "WARN",
            "propagate": False,
        },
    },
}

# Set else async logging to Sentry does not work
CELERY_QUEUES = {
    "default": {
        "exchange": "celery",
        "binding_key": "celery"
    },
    "sentry": {
        "exchange": "celery",
        "binding_key": "sentry"
    },
}

BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

SLACK_TOKEN = ""

import djcelery
djcelery.setup_loader()

try:
    import local_settings
    from local_settings import *
except ImportError:
    pass
else:
    if hasattr(local_settings, 'configure'):
        lcl = locals()
        di = local_settings.configure(**locals())
        lcl.update(**di)
