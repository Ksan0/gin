"""
Django settings for gin project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from .settings_local import SettingsLocal
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0@-d8&l98616fejd@9z)(i*z_i+^edh_b4%mo8z1or5%15937m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = SettingsLocal.DEBUG
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
    "." + SettingsLocal.DOMAIN_NAME
]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'subsystems.a_user',
    'subsystems.user',
    'subsystems.operator',
    'subsystems.task'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'gin.urls'

WSGI_APPLICATION = 'gin.wsgi.application'

# User
AUTH_USER_MODEL = 'a_user.AUser'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'localhost',
        'NAME': 'gindb',
        'PORT': '6432',
        'USER': 'ginuser',
        'PASSWORD': SettingsLocal.DB_PASSWORD
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR

STATICFILES_DIRS = (
  'static',
)

TEMPLATE_DIRS = [
    os.path.join(BASE_DIR, 'templates')
]


# email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = SettingsLocal.EMAIL_USER
EMAIL_HOST_PASSWORD = SettingsLocal.EMAIL_PASSWORD
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


class CustomSettings:
    DOMAIN_NAME_FULL = "http://" + SettingsLocal.DOMAIN_NAME