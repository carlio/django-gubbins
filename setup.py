# -*- coding: UTF-8 -*-
from distutils.core import setup
from setuptools import find_packages
import time

_version = "1.0"
_packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])
    
# common dependencies
_install_requires = [
            'django',
       ]

with open('README.md') as f:
    _long_description = f.read()

setup( name='django-gubbins',
       url='https://github.com/carlio/django-gubbins',
       author='Carl Crowder',
       author_email='django-gubbins@jqx.be',
       description='A collection of useful snippets for enhancing or replacing functionality within Django',
       long_description=_long_description,
       version=_version,
       packages=_packages,
       install_requires=_install_requires,
       license='BSD',
       keywords = "django",
)
