import settings

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'happyteam',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}

SECRET_KEY = 'vlzl-im4bp=i87!&3(2rfos^u7pa*286!-2!8v(j1m&z4#yqjj'

INTERNAL_IPS = ('127.0.0.1',)

#auto create new user if your firm email owner
EMAIL_VALIDATE = 'example.com'
EMAIL_VALIDATE = False

JABBER_ID = 'example@jabber.ru'
JABBER_PASSWORD = 'password'

NMAP_XML_URL = 'http://example.com/nmap.xml'

REPO_PATH = '/path/to/git/repo'

EMAIL_HOST_USER = ''
