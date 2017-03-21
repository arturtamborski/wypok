from django.core.wsgi import get_wsgi_application
import os
from .settings import DJANGO_SETTINGS_MODULE

os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)
application = get_wsgi_application()
