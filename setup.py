# -*- coding: UTF-8 -*-
from distutils.core import setup
from setuptools import find_packages
import time

_version = "1.1"
_packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])
    
# common dependencies
_install_requires = [
            'django>=1.3',
       ]

_long_description = """
django-gubbins is a collection of useful snippets for enhancing
or replacing functionality within Django. For more documentation, see the github
page at https://github.com/carlio/django-gubbins

Automatic downcasting to model subclasses :
This is for the case when you have a model hierarchy, with several models inheriting from
a base class, and you want to query the base class but get instances of the subclasses
out of the query set.

`EnumField` : provides an easy way to have a model field which only accepts 
some values, and at the same time makes it easy to reference those values in your code.

`JSONField` : allows you to store JSON strings in a database. 

`ReusableAppURLs` : a simple way to create the correct URL configuration for a reusable
django app.

`SlowFileUploadHandler` : can be used to really slow down handling of file uploads. 
This is an implementation of the Django file upload handler which will sleep between 
processing chunks in order to simulate a slow upload. This is intended for development 
when creating features such as an AJAXy file upload progress bar, as uploading to a 
local process is often too quick.
"""


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
