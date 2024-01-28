import os
import sys

# Set the path to your Django project directory
path = '/home/beelanci/public_html/beelancing'
if path not in sys.path:
    sys.path.append(path)

# Set the environment variable for the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'beelancing.settings'

# Import the Django WSGI handler
from django.core.wsgi import get_wsgi_application

# Define the WSGI application
application = get_wsgi_application()
