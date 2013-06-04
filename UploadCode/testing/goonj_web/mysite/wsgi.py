import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

path = '/usr/local/lib/python2.6/dist-packages/mysite'
if path not in sys.path:
    sys.path.append(path)

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

os.environ['CELERY_LOADER'] = 'django'

