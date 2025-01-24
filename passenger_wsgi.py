import os
import sys
from django.core.wsgi import get_wsgi_application

# Set the path to your project directory
project_path = '/home2/rasumcom/eudemia'
if project_path not in sys.path:
    sys.path.insert(0, project_path)

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eudemia.settings')

# Create the WSGI application
application = get_wsgi_application()
