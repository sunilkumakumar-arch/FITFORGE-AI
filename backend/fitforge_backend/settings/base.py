"""
Base Django settings for FitForge Backend.

Shared settings used by:
    - development.py
    - production.py

Environment-specific settings belong in their respective files.
"""

from pathlib import Path
from datetime import timedelta
import logging
import os

from dotenv import load_dotenv


# ==========================================================
# BASE DIRECTORY
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent


# ==========================================================
# ENVIRONMENT
# ==========================================================

load_dotenv(BASE_DIR / ".env")


# ==========================================================
# SECURITY
# ==========================================================

SECRET_KEY = os.environ["SECRET_KEY"]

DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv("ALLOWED_HOSTS", "").split(",")
    if host.strip()
]


# ==========================================================
# APPLICATIONS
# ==========================================================

INSTALLED_APPS = [
    # ------------------------------------------------------
    # Third-party applications
    # ------------------------------------------------------
    "corsheaders",
    "drf_spectacular",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "django_filters",
    "django_bootstrap5",

    # ------------------------------------------------------
    # Django applications
    # ------------------------------------------------------
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # ------------------------------------------------------
    # FitForge applications
    # ------------------------------------------------------
    "api",
    "audit",
    "users.apps.UsersConfig",
    "authentication",
    "authorization",
    "accounts",
    "core",
    "attendance",
    "trainers",
    "nutrition",
    "ai_coach",
    "gym_management",
    "dashboard",
    "member_hub",
    "memberships",
    "employees",
    "common",
    "billing",
    "workouts",
    "reports",
    "notifications",
    "roles",
    "trainer_assignments",
    "pt_packages",
    "leads",
    "certifications",
    "bootstrap",
    "reception",
    "general_training",
    "shared",
]


# ==========================================================
# MIDDLEWARE
# ==========================================================

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ==========================================================
# URL / WSGI
# ==========================================================

ROOT_URLCONF = "fitforge_backend.urls"

WSGI_APPLICATION = "fitforge_backend.wsgi.application"


# ==========================================================
# TEMPLATES
# ==========================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ==========================================================
# DATABASE
# ==========================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}


# ==========================================================
# PASSWORD VALIDATION
# ==========================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# ==========================================================
# INTERNATIONALIZATION
# ==========================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# ==========================================================
# STATIC / MEDIA
# ==========================================================

STATIC_URL = "static/"

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# ==========================================================
# CORS
# ==========================================================

CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ALLOWED_ORIGINS",
        "",
    ).split(",")
    if origin.strip()
]


# ==========================================================
# DRF SPECTACULAR / OPENAPI
# ==========================================================

SPECTACULAR_SETTINGS = {
    "TITLE": "FitForge Enterprise API",

    "DESCRIPTION": (
        "Enterprise-grade AI-powered Gym Management System API "
        "for Body Beast Gym and FitForge SaaS."
    ),

    "VERSION": "1.0.0",

    "SERVE_INCLUDE_SCHEMA": False,

    "SCHEMA_PATH_PREFIX": r"/api/v1",

    "COMPONENT_SPLIT_REQUEST": True,

    # ==========================================================
    # ENUM NAME OVERRIDES
    # ==========================================================
    #
    # IMPORTANT:
    # These names must be unique.
    # Do not define the same choice set under multiple names.
    #
    # ==========================================================

    "ENUM_NAME_OVERRIDES": {
        # ==========================================================
        # FITNESS GOALS
        # ==========================================================
        "GoalTypeEnum": [
            ("WEIGHT_LOSS", "Weight Loss"),
            ("FAT_LOSS", "Fat Loss"),
            ("MUSCLE_GAIN", "Muscle Gain"),
            ("STRENGTH", "Strength"),
            ("GENERAL_FITNESS", "General Fitness"),
        ],

        # ==========================================================
        # PAYMENT METHODS
        # ==========================================================
        "PaymentMethodEnum": [
            ("Cash", "Cash"),
            ("UPI", "UPI"),
            ("Card", "Card"),
            ("Bank Transfer", "Bank Transfer"),
        ],

        # ==========================================================
        # EMPLOYEE EMPLOYMENT STATUS
        # ==========================================================
        "EmployeeEmploymentStatusEnum": [
            ("ACTIVE", "Active"),
            ("ON_LEAVE", "On Leave"),
            ("SUSPENDED", "Suspended"),
            ("TERMINATED", "Terminated"),
        ],

        # ==========================================================
        # TRAINER EMPLOYMENT STATUS
        # ==========================================================
        "TrainerEmploymentStatusEnum": [
            ("Active", "Active"),
            ("Inactive", "Inactive"),
            ("On Leave", "On Leave"),
            ("Terminated", "Terminated"),
        ],

        # ==========================================================
        # TRAINER SHIFT
        #
        # Trainer.SHIFT_CHOICES and TrainerProfile.SHIFT_CHOICES
        # contain this same choice set.
        # ==========================================================
        "TrainerShiftTypeEnum": [
            ("SHIFT_1", "6AM-10:30AM & 5PM-9:30PM"),
            ("SHIFT_2", "6AM-10:30AM & 5:30PM-10PM"),
            ("SHIFT_3", "6AM-3PM"),
            ("SHIFT_4", "1PM-10PM"),
            ("SHIFT_5", "5:30AM-2:30PM"),
            ("SHIFT_6", "12PM-9PM"),
        ],

        # ==========================================================
        # CORE SHIFT TYPE
        # ==========================================================
        "CoreShiftTypeEnum": [
            ("GENERAL", "General"),
            ("MORNING", "Morning"),
            ("EVENING", "Evening"),
            ("NIGHT", "Night"),
            ("FLEXIBLE", "Flexible"),
            ("SPLIT", "Split"),
        ],
    },

    # ==========================================================
    # SWAGGER UI
    # ==========================================================

    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "displayOperationId": True,
        "displayRequestDuration": True,
        "persistAuthorization": True,
    },

    # ==========================================================
    # AUTHENTICATION
    # ==========================================================

    "SECURITY": [
        {
            "BearerAuth": [],
        }
    ],

    "SECURITY_SCHEMES": {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    },

    # ==========================================================
    # API TAGS
    # ==========================================================

    "TAGS": [
        {
            "name": "Authentication",
            "description": "Authentication APIs",
        },
        {
            "name": "Accounts",
            "description": "Member & Employee APIs",
        },
        {
            "name": "Memberships",
            "description": "Membership Management",
        },
        {
            "name": "Attendance",
            "description": "Attendance Management",
        },
        {
            "name": "Billing",
            "description": "Payments & Billing",
        },
        {
            "name": "Workouts",
            "description": "Workout Management",
        },
        {
            "name": "Nutrition",
            "description": "Nutrition Management",
        },
        {
            "name": "Dashboard",
            "description": "Dashboard & Analytics",
        },
        {
            "name": "Reports",
            "description": "Reports",
        },
    ],
}


# ==========================================================
# SIMPLE JWT
# ==========================================================

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),

    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),

    "ROTATE_REFRESH_TOKENS": True,

    "BLACKLIST_AFTER_ROTATION": True,

    "UPDATE_LAST_LOGIN": True,

    "ALGORITHM": "HS256",

    "SIGNING_KEY": SECRET_KEY,

    "AUTH_HEADER_TYPES": ("Bearer",),
}


# ==========================================================
# DJANGO REST FRAMEWORK
# ==========================================================

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),

    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),

    "EXCEPTION_HANDLER": (
        "common.exceptions.fitforge_exception_handler"
    ),

    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ),

    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/hour",
        "user": "1000/hour",
        "login": "10/minute",
        "logout": "30/minute",
        "change_password": "10/minute",
    },

    "DEFAULT_SCHEMA_CLASS": (
        "drf_spectacular.openapi.AutoSchema"
    ),

    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),

    "DEFAULT_PAGINATION_CLASS": (
        "rest_framework.pagination.PageNumberPagination"
    ),

    "PAGE_SIZE": 20,
}


# ==========================================================
# SECURITY HEADERS
# ==========================================================

X_FRAME_OPTIONS = "DENY"

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

SECURE_BROWSER_XSS_FILTER = True

CSRF_COOKIE_HTTPONLY = True

SESSION_COOKIE_HTTPONLY = True


# ==========================================================
# DEVELOPMENT / PRODUCTION SECURITY DEFAULTS
# ==========================================================

# These are safe development defaults.
# production.py should override them when HTTPS is enabled.

SECURE_SSL_REDIRECT = False

SESSION_COOKIE_SECURE = False

CSRF_COOKIE_SECURE = False

SECURE_HSTS_SECONDS = 0

SECURE_HSTS_INCLUDE_SUBDOMAINS = False

SECURE_HSTS_PRELOAD = False


# ==========================================================
# LOGGING
# ==========================================================

LOG_DIR = BASE_DIR / "logs"

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


LOGGING = {
    "version": 1,

    "disable_existing_loggers": False,

    "formatters": {
        "standard": {
            "format": "[{asctime}] {levelname} {name}: {message}",
            "style": "{",
        },
    },

    "handlers": {
        "info_file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": LOG_DIR / "info.log",
            "formatter": "standard",
        },

        "error_file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": LOG_DIR / "error.log",
            "formatter": "standard",
        },

        "security_file": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": LOG_DIR / "security.log",
            "formatter": "standard",
        },

        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },

    "root": {
        "handlers": [
            "console",
            "info_file",
            "error_file",
        ],

        "level": "INFO",
    },

    "loggers": {
        "django.security": {
            "handlers": [
                "security_file",
                "console",
            ],

            "level": "WARNING",

            "propagate": False,
        },

        "roles.permissions": {
            "handlers": [
                "security_file",
                "console",
            ],

            "level": "WARNING",

            "propagate": False,
        },
    },
}