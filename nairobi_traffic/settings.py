import os
from pathlib import Path
import dj_database_url

# --- Configuration Helper ---
# This looks for variables in your environment (Cloud) or a .env file (Local)
try:
    from decouple import config
except ModuleNotFoundError:
    def config(key, default=None, cast=None):
        value = os.getenv(key, default)
        if value is None: return default
        if cast and callable(cast): return cast(value)
        return value

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Security ---
# On the cloud, set DEBUG to False in your environment variables
SECRET_KEY = config('SECRET_KEY', default='django-insecure-dev-key-change-this-in-prod')
DEBUG = config('DEBUG', default=True, cast=bool)

# Cloud platforms provide a specific hostname; we catch it here
ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS', 
    default='localhost,127.0.0.1', 
    cast=lambda v: [s.strip() for s in v.split(',')]
)
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# --- Application Definition ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', # Helps whitenoise serve static files in dev
    'django.contrib.staticfiles',
    'traffic.apps.TrafficConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Essential for cloud CSS/JS
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'nairobi_traffic.urls'

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
                'django.template.context_processors.media', 
            ],
        },
    },
]

WSGI_APPLICATION = 'nairobi_traffic.wsgi.application'

# --- Database ---
# This logic checks if a DATABASE_URL exists (Cloud/Postgres) 
# otherwise it defaults to your local SQLite.
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=600
    )
}

# --- Authentication Redirects ---
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = 'login'

# --- Internationalization ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_TZ = True

# --- Static & Media Files ---
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# This enables WhiteNoise to compress and cache your CSS/JS for speed
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Deployment Security ---
# This prevents 403 Forbidden errors when submitting forms on the live site
CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS', 
    default='https://*.onrender.com,https://*.herokuapp.com', 
    cast=lambda v: [s.strip() for s in v.split(',')]
)
if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f"https://{RENDER_EXTERNAL_HOSTNAME}")