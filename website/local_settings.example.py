import os
from website.settings import SITE_ROOT

# sqlite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(SITE_ROOT, 'db/db.sqlite3'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        }
}

# PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db_name',
        'USER': 'db_user',
        'PASSWORD': 'db_password',
        'HOST': 'localhost',
        'PORT': '',
        }
}

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'INSERT_UNIQUE_SECRET_KEY_HERE'

#auto create new user if your firm email owner
EMAIL_VALIDATE  = 'example.com'
EMAIL_VALIDATE  = False

JABBER_ID = 'example@jabber.ru'
JABBER_PASSWORD = 'password'

NMAP_XML_URL = 'http://example.com/nmap.xml'

REPO_PATH = '/path/to/git/repo'

EMAIL_HOST_USER = ''
