#!/usr/bin/env python

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inventar.settings")
# if needed:
# sys.path.insert(0, "/var/www/ktt-inventory-system")

application = get_wsgi_application()