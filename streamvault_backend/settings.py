import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # ← THIS was missing!

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-dev-key-change-in-production')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'streamvault_backend.urls'
TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates','DIRS': [],'APP_DIRS': True,'OPTIONS': {'context_processors': ['django.template.context_processors.debug','django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages']}}]
WSGI_APPLICATION = 'streamvault_backend.wsgi.application'

DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3','NAME': BASE_DIR / 'db.sqlite3'}}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
    'DEFAULT_THROTTLE_CLASSES': ['rest_framework.throttling.AnonRateThrottle'],
    'DEFAULT_THROTTLE_RATES': {'anon': '200/hour'}
}

TMDB_API_KEY = os.environ.get('TMDB_API_KEY', '')
TMDB_BASE_URL = 'https://api.themoviedb.org/3'

# Streaming embed providers
VIDSRC_BASE_URL = os.environ.get('VIDSRC_BASE_URL', 'https://vidsrc.xyz/embed/movie')
VIDSRC_TO_BASE_URL = os.environ.get('VIDSRC_TO_BASE_URL', 'https://vidsrc.to/embed/movie')
EMBED2_BASE_URL = os.environ.get('EMBED2_BASE_URL', 'https://www.2embed.cc/embedtv')
VIDSRC_ME_BASE_URL = os.environ.get('VIDSRC_ME_BASE_URL', 'https://vidsrc.me/embed/movie')
MOVIES123_BASE_URL = os.environ.get('MOVIES123_BASE_URL', 'https://movies123.to/embed/movie')
PUTLOCKER_BASE_URL = os.environ.get('PUTLOCKER_BASE_URL', 'https://putlocker.to/embed/movie')
SOLARMOVIE_BASE_URL = os.environ.get('SOLARMOVIE_BASE_URL', 'https://solarmovie.to/embed/movie')
FMOVIES_BASE_URL = os.environ.get('FMOVIES_BASE_URL', 'https://fmovies.to/embed/movie')