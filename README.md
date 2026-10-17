# KtT Inventory System

A simple Django app that tracks our inventory.

## Setup

1. Create a venv, e.g. 

```shell
apt-get install python3-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd inventory/static/ && ln -s ../../venv/lib/python3.*/site-packages/django/contrib/admin/static/admin && cd -
```

## Development

All steps assume that you've activated the venv, e.g. `source venv/bin/activate`.

Create the database tables (first time only):

```shell
./manage.py migrate
```

Start the local dev server with

```shell
./manage.py runserver
```

## Testing

Run the test suite with:

```shell
pytest
```

Tests use pytest-django. A session-scoped baseline populates the
database once with sample inventory data (`tests/conftest.py`).
Most tests run against this baseline. Tests that need an empty
database request the `empty_db` fixture.

## Configuration

### `BARCODE_CODE_LENGTH`

Tuple of `(min, max)` controlling the accepted barcode code length
in the UI. Affects the search input `maxlength` attribute and the
URL pattern for item lookup. Defaults to `(4, 6)` when not set.

```python
BARCODE_CODE_LENGTH = (4, 8)
```

Nothing checks this range when a code is saved. `Barcode.code`
accepts up to 10 characters either way.

A code outside the range has no URL of its own. Looking it up
returns 404. The item is still linked, by its id. Set the range to
cover the codes you use.

## Server

```shell
apt install nginx uwsgi uwsgi-plugin-python3
```

/etc/uwsgi/apps-enabled/ktt-inventar.ini
```ini
[uwsgi]
plugin          = python3
virtualenv      = /var/www/ktt-inventory-system/venv
pythonpath      = /var/www/ktt-inventory-system/venv

chdir           = /var/www/ktt-inventory-system
wsgi-file       = /var/www/ktt-inventory-system/inventory-wsgi.py

#uid = www-data
#gid = www-data

# process-related settings
# master
master          = true
# maximum number of worker processes
processes       = 2

# the socket (use the full path to be safe
#socket = /run/uwsgi/app/ifs/socket
#chown-socket = www-data:www-data
#chmod-socket = 664
```

/etc/nginx/sites-enabled/ktt-inventory
```
server {
        listen 82 default_server;
        listen [::]:82 default_server;

        root /var/www/ktt-inventory-system/inventory;
        index index.html index.htm;

        # static files are not passed to uwsgi
        location /media {
        }
        location /static {
        }
        location /other {
        }
        location /uploaded {
                alias /var/www/ktt-inventory-system/uploaded;
        }

        location /robots.txt {
                alias /var/www/robots.txt;
        }

        location / {
                gzip off;
                client_max_body_size 20M;
                include uwsgi_params;
                uwsgi_pass unix:/run/uwsgi/app/ktt-inventar/socket;
        }
}
```