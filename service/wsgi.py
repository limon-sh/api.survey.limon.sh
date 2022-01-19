import os

from whitenoise import WhiteNoise
from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.production')

application = WhiteNoise(get_wsgi_application())
