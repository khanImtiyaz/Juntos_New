import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = True

####For Postgres Setiing would be
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'JuntosDummy',
        'USER': 'saket.gupta',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
        }
}