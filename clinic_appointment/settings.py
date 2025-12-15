"""
Django settings for clinic_appointment project.
"""

from pathlib import Path
from decouple import config
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
# Railway: Set DEBUG=False in Railway environment variables for production
# Local development: DEBUG=True (default)
# Production: DEBUG=False (set in Railway environment variables)
DEBUG = config('DEBUG', default=True, cast=bool)

# ALLOWED_HOSTS Configuration
# Railway: Add your Railway domain to ALLOWED_HOSTS via environment variable
# Example Railway domain: web-production-8531f.up.railway.app
# Local development: localhost, 127.0.0.1 (default)
# Production: Set ALLOWED_HOSTS in Railway environment variables
# Format: "web-production-8531f.up.railway.app,127.0.0.1,localhost"
# Or use wildcard: "*.up.railway.app,*.railway.app,127.0.0.1,localhost"

# Get ALLOWED_HOSTS from environment variable
allowed_hosts_str = config('ALLOWED_HOSTS', default='')

if allowed_hosts_str:
    # Use environment variable if provided
    ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_str.split(',') if host.strip()]
else:
    # Default: localhost for development
    if DEBUG:
        ALLOWED_HOSTS = ['localhost', '127.0.0.1']
    else:
        # Production: Include Railway domains by default
        # Specific Railway domain: web-production-8531f.up.railway.app
        ALLOWED_HOSTS = [
            '127.0.0.1',
            'localhost',
            'web-production-8531f.up.railway.app',
            '*.up.railway.app',
            '*.railway.app',
        ]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'djoser',
    'drf_spectacular',  # OpenAPI/Swagger documentation
    
    # Local apps
    'accounts',
    'appointments',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'clinic_appointment.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'clinic_appointment.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# Railway deployment: Use DATABASE_URL if available (Railway provides this automatically)
# Local development: Falls back to SQLite or individual DB settings
DATABASE_URL = config('DATABASE_URL', default=None)

if DATABASE_URL:
    # Production: Railway provides DATABASE_URL automatically
    # Format: postgresql://user:password@host:port/dbname
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    # Development: Use individual settings or SQLite fallback
    DB_ENGINE = config('DB_ENGINE', default='sqlite')
    
    if DB_ENGINE == 'postgresql':
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': config('DB_NAME', default='clinic_appointment_db'),
                'USER': config('DB_USER', default='postgres'),
                'PASSWORD': config('DB_PASSWORD', default='postgres'),
                'HOST': config('DB_HOST', default='localhost'),
                'PORT': config('DB_PORT', default='5432'),
            }
        }
    else:
        # SQLite fallback for local development
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }


# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django REST Framework settings
# REFACTOR: Disabled browsable API - using JSONRenderer only to prevent patients from seeing API errors
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    # Disable browsable API - only return JSON
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
}

# JWT Settings
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# Djoser Settings
DJOSER = {
    'LOGIN_FIELD': 'email',
    'USER_CREATE_PASSWORD_RETYPE': True,
    'SERIALIZERS': {
        'user_create': 'accounts.serializers.UserCreateSerializer',
        'user': 'accounts.serializers.UserSerializer',
        'current_user': 'accounts.serializers.UserSerializer',
    },
    'PERMISSIONS': {
        'user': ['rest_framework.permissions.IsAuthenticated'],
        'user_list': ['rest_framework.permissions.IsAdminUser'],
    },
}

# CORS Settings
# Railway: Configure CORS for production domain
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    # Production: Allow Railway domain and any specified origins
    CORS_ALLOWED_ORIGINS = config(
        'CORS_ALLOWED_ORIGINS',
        default='',
        cast=lambda v: [s.strip() for s in v.split(',') if s.strip()]
    )
    # If no origins specified, allow Railway domains
    if not CORS_ALLOWED_ORIGINS:
        CORS_ALLOWED_ORIGINS = [
            "https://*.up.railway.app",
            "https://*.railway.app",
        ]

CORS_ALLOW_CREDENTIALS = True

# CSRF Settings for Railway
# Railway: Add your Railway domain to CSRF_TRUSTED_ORIGINS via environment variable
# Example: "https://web-production-8531f.up.railway.app"
# Or use wildcard: "https://*.up.railway.app,https://*.railway.app"
csrf_origins_str = config('CSRF_TRUSTED_ORIGINS', default='')

if csrf_origins_str:
    # Use environment variable if provided
    CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in csrf_origins_str.split(',') if origin.strip()]
else:
    # Default: No CSRF trusted origins for development
    if DEBUG:
        CSRF_TRUSTED_ORIGINS = []
    else:
        # Production: Trust Railway domains by default
        CSRF_TRUSTED_ORIGINS = [
            "https://*.up.railway.app",
            "https://*.railway.app",
        ]

# WhiteNoise settings for static files
# Railway: WhiteNoise serves static files in production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Production Security Settings (Railway)
# These are only applied when DEBUG=False
if not DEBUG:
    # HTTPS Security
    SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'

# drf-spectacular (OpenAPI/Swagger) Settings
# Railway: API documentation available at /api/docs/ and /api/redoc/
SPECTACULAR_SETTINGS = {
    'TITLE': 'Apex Dental Care - Appointment Manager API',
    'DESCRIPTION': 'Complete API documentation for Apex Dental Care Clinic Appointment Management System',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': '/api/',
    'TAGS': [
        {'name': 'Authentication', 'description': 'JWT authentication and user registration'},
        {'name': 'Appointments', 'description': 'Appointment management endpoints'},
        {'name': 'Users', 'description': 'User and profile management'},
        {'name': 'Visit History', 'description': 'MongoDB visit history records'},
    ],
    # Use drf-spectacular's AutoSchema for all ViewSets
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

