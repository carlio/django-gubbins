# django-gubbins

[![Build Status](https://secure.travis-ci.org/carlio/django-gubbins.png)](http://travis-ci.org/carlio/django-gubbins)

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
	
    class MyBaseModel(models.Model):
    	manager = InheritanceManager()
     	... 
     
From now on any queryset on `MyBaseModel` will correctly downcast to the subclass.

See http://jeffelmore.org/tag/django-python-inheritance-downcasting-orm-polymorphism-queryset/


## EnumField 

`EnumField` provides an easy way to have a model field which only accepts some values, and at the same
time makes it easy to reference those values in your code.

Usage example:

    from gubbins.db.field import EnumField
    
    class FruitField(EnumField):
        BANANA = 'b'
        APPLE = 'a'
        TOMATO = 't'
    
    class MyLovelyModel(models.Model):
        fruit = FruitField(null=True, default=FruitField.BANANA)
        ...
          
          
An `EnumField` is simply a standard Django `CharField` with some additional helping methods.

You can use the constants defined on your field class throughout your code, thus improving
readability and 

    def make_everything_apples():
        MyLovelyModel.objects.update(fruit=FruitField.APPLE)
        return 'mmm'
        
Note: the names of the values on your class must be entirely uppercase or they will be ignored.

You can pass any arguments into the constructor, and they will be passed on to `CharField`, with
two excpetions: firstly, `choices` is set automatically so you cannot specify it yourself. Secondly,
`max_length` will be adhered to after a sanity check to ensure all of the defined values can fit.
If `max_length` is not specified, then the length of the largest value will be used. 

Using an unspecified value will result in a `ValueError` when trying to save the model:

    >>> m = MyLovelyModel()
    >>> m.fruit = 'carrot'
    >>> m.save()
      ...
    ValueError: carrot is not an acceptable value for this field
    

        
## JSONField

`gubbins.db.field.JSONField` allows you to store JSON strings in a database. It automatically uses `json.loads` and `json.dumps` to convert to and from strings.

This was taken from the `django-annoying` project due to various shortcomings in the original and the lack of activity on [the original repo](https://bitbucket.org/offline/django-annoying); hopefully this version will fix and improve upon the original.

Usage:

    from gubbins.db.field import JSONField

    class MyLovelyModel(models.Model):
        some_data  = JSONField()
    
    # you can set a dictionary as the value and it will be automatically converted    
    >>> my_model = MyLovelyModel()
    >>> my_model.some_data = {'a': 1, 'b': 'fish', 'woo': [1, 'f', 5]}
    >>> my_model.save()
    
    # the values will be available as dictionaries once again after loading
    >>> my_model = MyLovelyModel.objects.get(pk=1)
    >>> print my_model.some_data['woo'][1:]
    ['f', 5]
    

Note that there are likely to be several outstanding bugs (for example you can't correctly update JSON fields in the admin), please file an issue if you find one.


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