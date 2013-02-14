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