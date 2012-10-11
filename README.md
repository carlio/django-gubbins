# django-gubbins

Django Gubbins is a collection of useful snippets for enhancing
or replacing functionality within Django.

## Automatic downcasting to model subclasses

See `gubbins.db.queryset.InheritanceQuerySet` and `gubbins.db.manager.IneritanceManager`

## `EnumField` 

`gubbins.db.field.EnumField`

## `JSONField`

`gubbins.db.field.JSONField`


## URLs

`ReusableAppURLs` is a simple way to create the correct URL configuration for a reusable
django app.


Usage:

    myapp/__init__.py
       urlpatterns = ...
       urls = ReusableApp('myapp', urlpatterns)


    project_name/urls.py
       urlpatterns = patterns(r'^path/', myapp.urls())

       # or with instance namespace
       urlpatterns = patterns(r'^path/', myapp.urls('myapp1'))