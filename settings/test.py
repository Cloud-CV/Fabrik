from .common import * # noqa: ignore=F405

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'fabrik',
        'USER': 'admin',
        'PASSWORD': 'fabrik',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}

TEST = True
