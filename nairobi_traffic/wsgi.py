"""
WSGI config for nairobi_traffic project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nairobi_traffic.settings')

application = get_wsgi_application()