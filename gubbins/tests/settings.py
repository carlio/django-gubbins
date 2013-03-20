
INSTALLED_APPS = ['gubbins', 'gubbins.db.tests']

try:
    import django_jenkins
except ImportError:
    pass
else:
    INSTALLED_APPS += ['django_jenkins']

SECRET_KEY='gubbins_tests'

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

