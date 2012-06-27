
INSTALLED_APPS = ['django_jenkins', 'gubbins', 'gubbins.db.tests']
PROJECT_APPS = ['gubbins']

DATABASES = {
        'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
                'USER': '',
                'PASSWORD': '',
                'HOST': '',
                'PORT': '',
        }
}

