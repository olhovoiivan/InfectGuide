import os
from pathlib import Path

# Побудова шляхів (BASE_DIR вказує на корінь проєкту)
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: тримайте ключ у секреті для реальних проєктів!
SECRET_KEY = "django-insecure-6po*&_cxs=qx)lr9i#txpsmif=tkpoxvee11ww@_)3lj30j4zd"

# SECURITY WARNING: на Render краще вимикати DEBUG, але для лаби можна залишити True
DEBUG = True

ALLOWED_HOSTS = ['infectguide.onrender.com', '127.0.0.1', 'localhost', '.onrender.com']

# Визначення застосунків
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'diseases', # Твій основний додаток
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # ДОДАНО ДЛЯ СТИЛІВ НА RENDER
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'], # Дозволяє шукати шаблони в папці templates
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

WSGI_APPLICATION = "core.wsgi.application"

# База даних (SQLite3 за замовчуванням)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Валідація паролів
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Налаштування мови та часу
LANGUAGE_CODE = "uk-ua" # Змінив на українську для зручності
TIME_ZONE = "Europe/Kyiv"
USE_I18N = True
USE_TZ = True

# --- НАЛАШТУВАННЯ СТАТИКИ ТА МЕДІА ---

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] # Де лежать твої стилі під час розробки

# Папка, куди Render збере всі стилі для WhiteNoise
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Використання WhiteNoise для зберігання статики (щоб адмінка була красивою)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Авторизація
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"