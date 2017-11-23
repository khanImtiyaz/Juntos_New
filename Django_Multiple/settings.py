"""
Django settings for Django_Multiple project.

Generated by 'django-admin startproject' using Django 1.11.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zoxd%l@)cn6_!+s4)79&*p@!_5*akl-phfbyjyu$6z(%bk4no+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]
# JET_DEFAULT_THEME = 'green'
JET_SIDE_MENU_COMPACT = True

# Application definition

INSTALLED_APPS = [
    'material.theme.yellow',
    'material',
    'material.admin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'templated_email',
    'social_django',
    'cloudinary',
    'ckeditor',
    'Juntos',
    'Vendor',
    'Static_Model',
    'Log',
    'nested_admin',
    'nested_inline',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    # 'Django_Multiple.middleware.LoggingMiddleware'

]

ROOT_URLCONF = 'Django_Multiple.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'Juntos.context_processors.categoriesData',
                'Juntos.context_processors.about',
                'Juntos.context_processors.starRating',
                'Juntos.context_processors.cart',
                'Juntos.context_processors.userShippingDetail',
                'Juntos.context_processors.unreadCount',
                'Juntos.context_processors.bannerList',
                'Juntos.context_processors.newsSection',
                'Juntos.context_processors.taxValue'
            ],
        },
    },
]

WSGI_APPLICATION = 'Django_Multiple.wsgi.application'
TEMPLATED_EMAIL_TEMPLATE_DIR = 'templated_email/' #use '' for top level template dir, ensure there is a trailing slash
TEMPLATED_EMAIL_FILE_EXTENSION = 'email'

ALLOWED_HOSTS = ['*']



# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'JuntosDummy',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
        }
}

AUTH_USER_MODEL = 'Juntos.MyUser'
SOCIAL_AUTH_USER_MODEL = AUTH_USER_MODEL
SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    'Juntos.social.social'
)
SOCIAL_AUTH_REDIRECT_IS_HTTPS = False
SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_FACEBOOK_KEY = '124276874915287' #'1388477681224546' 
SOCIAL_AUTH_FACEBOOK_SECRET = '1173fd503fb0bfa6ac39964bfd75d10b' #'8ebfd05c376d3108fbae7163c366daf1'
SOCIAL_AUTH_ENABLED_BACKENDS = ('facebook')
SOCIAL_AUTH_FORCE_EMAIL_VALIDATION = True
SOCIAL_AUTH_FACEBOOK_SCOPE  = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {'fields': 'id,email,first_name,last_name',}
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = '/'
AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CLOUDINARY = {
    'cloud_name': 'imtiyaz',
    'api_key': '881311727223736',
    'api_secret': '_9BMYEdz3XJ8QNS327r30MM6ISQ',
    'secure':False,
    'max_length': 200,
}

STATIC_URL  = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static_cdn")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
MEDIA_ROOT = 'media/'
MEDIA_URL = 'http://127.0.0.1:8000/media/'

# It is only used for Development Purpose
# try:
#     from .local_settings import *
# except ImportError:
#     pass

