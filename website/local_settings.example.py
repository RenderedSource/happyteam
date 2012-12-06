import os
from website.settings import SITE_ROOT

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
#auto create new user if your firm email owner
EMAIL_VALIDATE  = 'example.com'
EMAIL_VALIDATE  = False

JABBER_ID = 'example@jabber.ru'
JABBER_PASSWORD = 'password'

NMAP_XML_URL = 'http://example.com/nmap.xml'

REPO_PATH = '/path/to/git/repo'

EMAIL_HOST_USER = ''
