from .base import *
import os


# ============================================================
# FITFORGE PRODUCTION SETTINGS
# ============================================================

DEBUG = False


# ------------------------------------------------------------
# Allowed Hosts
# ------------------------------------------------------------

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv("ALLOWED_HOSTS", "").split(",")
    if host.strip()
]


# ------------------------------------------------------------
# HTTPS / Security
# ------------------------------------------------------------

SECURE_SSL_REDIRECT = True

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

X_FRAME_OPTIONS = "DENY"

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_REFERRER_POLICY = "same-origin"


# ------------------------------------------------------------
# CSRF
# ------------------------------------------------------------

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]


# ------------------------------------------------------------
# CORS
# ------------------------------------------------------------

CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
    if origin.strip()
]

CORS_ALLOW_ALL_ORIGINS = False


# ------------------------------------------------------------
# Static / Media
# ------------------------------------------------------------

STATIC_ROOT = BASE_DIR / "staticfiles"


# ------------------------------------------------------------
# Production logging
# ------------------------------------------------------------

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
        "level": "INFO",
    },
}