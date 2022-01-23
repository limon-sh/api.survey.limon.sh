import os
from glob import glob


DEBUG = True

ROOT_URLCONF = 'api.urls'

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'change_me')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTALLED_APPS = [
    # Django apps
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',

    # Required apps
    'drf_yasg',
    'corsheaders',
    'rest_framework',
    'django_extensions',

    # Project apps
    'apps.survey'
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CONN_MAX_AGE = 60
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['POSTGRES_DB'],
        'HOST': os.environ['POSTGRES_HOST'],
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
        'USER': os.environ['POSTGRES_USER'],
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', '')
    }
}

TEMPLATES = (
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': glob('apps/**/templates/', recursive=True),
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
)

REST_FRAMEWORK = {
    'DATE_FORMAT': '%Y-%m-%d',
    'TIME_FORMAT': '%H:%M:%S',
    'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%SZ'
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOST', '*')

HOST = os.environ.get('HOST', 'http://0.0.0.0:8000')

CORS_ORIGIN_ALLOW_ALL = True

STATIC_DIR = 'static'
STATIC_URL = f'/{STATIC_DIR}/'
STATIC_ROOT = os.path.join(BASE_DIR, STATIC_DIR)

MEDIA_DIR = 'media'
MEDIA_URL = f'/{MEDIA_DIR}/'
MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_DIR)

USE_I18N = False

USE_TZ = True
TIME_ZONE = 'UTC'

SHELL_PLUS_PRINT_SQL = True
SHELL_PLUS_PRINT_SQL_TRUNCATE = None
SHELL_PLUS_SQLPARSE_FORMAT_KWARGS = {"reindent_aligned": True}
