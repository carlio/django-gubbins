# django-gubbins

Django Gubbins is a collection of useful snippets for enhancing
or replacing functionality within Django.

## Automatic downcasting to model subclasses

This is for the case when you have a model hierarchy, with several models inheriting from
a base class, and you want to query the base class but get instances of the subclasses
out of the query set.

Example:

    class MyBaseModel(models.Model):
        ... fields ...
        def some_function(self):
            return 'base!'
            
    class MyModel(MyBaseModel):
        ... fields ...
        def some_function(self):
            return 'subclass'
            
    class MyModel2(MyBaseModel):
    	... fields ...
        def some_function(self):
            return 'subclass2'
            
With the standard Django `Manager`, querying `MyBaseModel` will return `MyBaseModel` instances,
so that `some_function` will return `base!`. If you want to be able to get an instance of
`MyModel` or `MyModel2` instead, you can use the `InheritanceManager`:

	from gubbins.db.manager import InheritanceManager
	
    class MyBaseModel(models.Model)
    	manager = InheritanceManager()
     	... 
     
From now on any queryset on `MyBaseModel` will correctly downcast to the subclass.

See http://jeffelmore.org/tag/django-python-inheritance-downcasting-orm-polymorphism-queryset/


## EnumField 

`gubbins.db.field.EnumField`

## JSONField

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