from django.core.exceptions import ImproperlyConfigured
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
import json
import re


meta_super_class = type
try:
    # Django version 1.3 used this class for metaclasses of fields,
    # which results in an error when trying to use the EnumMeta
    # metaclass instead:
    #
    #       metaclass conflict: the metaclass of a derived class must be 
    #       a (non-strict) subclass of the metaclasses of all its bases
    #
    # This is because using EnumMeta causes fields to have two 'metaclass'
    # definitions when using Django 1.3. The solution is to have EnumMeta
    # be a subclass of LegacyConnection, but this is only possible in 1.3
    # as in 1.4, Legacy Connection was removed
    from django.db.models.fields.subclassing import LegacyConnection
    meta_super_class = LegacyConnection
except ImportError:
    pass

class EnumMeta(meta_super_class):
    
    def __new__(cls, name, bases, attrs):
        inst = meta_super_class.__new__(cls, name, bases, attrs)
        inst.options = EnumMeta._get_options(inst)
        inst.values = EnumMeta._get_values(inst)
        inst.choices = zip(inst.values, inst.options)
        return inst
    
    @staticmethod
    def _get_options(inst):
        """
        Gets the list of possible options for this object.
        """
        options = []
        
        for attr_name in dir(inst):
            if attr_name.startswith('_'):
                # ignore any 'private' attributes
                continue
            if not re.match('^[A-Z][A-Z0-9_]+$', attr_name):
                # ignore anything which is not all uppercase
                continue
            attr = getattr(inst, attr_name)
            if callable(attr):
                # ignore anything which is not a simple value
                continue
            options.append(attr_name)
        
        return options

    @staticmethod
    def _get_values(inst):
        return [ getattr(inst, attr_name) for attr_name in inst.options ]



class EnumField(models.CharField):
    """
    
    Example usage::

      class SourceType(EnumField):
          WIKIPEDIA = 'w'
          BBC_NEWS = 'b'
          TWITTER = 't'
    
    Note that field names must be uppercase to be recognised
    as possible field values
    
    """
    __metaclass__ = EnumMeta
    
    def __init__(self, *args, **kwargs):
        kwargs = self._get_field_kwargs(kwargs)
        super(EnumField, self).__init__(*args, **kwargs)
    
    def __getattr__(self, name):
        if self.options is not None and name in self.options:
            return name
        raise AttributeError('No such enum option: %s' % name)
    
    def _get_field_kwargs(self, kwargs):
        max_length = max( map(len, map(str, self.values) ) )
        if 'max_length' in kwargs:
            if kwargs['max_length'] < max_length:
                raise ImproperlyConfigured('Supplied max_length is too short, enum values will be truncated! It should be %s or unspecified to be set automatically' % max_length)
        else:
            kwargs['max_length'] = max_length
        
        if 'choices' in kwargs:
            raise ImproperlyConfigured('"choices" keyword argument is not used as it is automatically generated')
        kwargs['choices'] = self.choices
        
        return kwargs
    
    def get_prep_value(self, value):
        if value not in [None, ''] + self.values:
            raise ValueError('%s is not an acceptable value for this field' % value)
        return super(EnumField, self).get_prep_value(value)
    
    def south_field_triple(self):
        # see http://south.readthedocs.org/en/latest/customfields.html#south-field-triple
        module = self.__class__.__module__
        field_name = self.__class__.__name__
        return ('%s.%s' % (module, field_name), [], {})




class JSONField(models.TextField):
    """
    JSONField is a generic textfield that neatly serializes/unserializes
    JSON objects seamlessly.
    Django snippet #1478

    example:
        class Page(models.Model):
            data = JSONField(blank=True, null=True)


        page = Page.objects.get(pk=5)
        page.data = {'title': 'test', 'type': 3}
        page.save()
    """
    # origially cribbed from django-annoying, which seems to have lain dormant
    # for a while and no pull requests are getting merged in

    __metaclass__ = models.SubfieldBase

    class CannotStoreTypeException(Exception):
        def __init__(self, type_):
            self._type = type_
        def __repr__(self):
            return 'Cannot store type in a JSONField: %s' % self._type

    def to_python(self, value):
        if value == "":
            return None

        try:
            if isinstance(value, basestring):
                return json.loads(value)
        except ValueError:
            pass 
        # TODO: this is shitty behaviour, should be fixed, but what should the
        # field do if the value in the database is invalid?
        return value

    def get_db_prep_save(self, value, *args, **kwargs):
        if value == "":
            return None
        
        # see what dummy key we need to use
        if not isinstance(value, (list, dict)):
            raise JSONField.CannotStoreTypeException(type(value))

        value = json.dumps(value, cls=DjangoJSONEncoder)
        return super(JSONField, self).get_db_prep_save(value, *args, **kwargs)
    
    def south_field_triple(self):
        # see http://south.readthedocs.org/en/latest/customfields.html#south-field-triple
        module = self.__class__.__module__
        field_name = self.__class__.__name__
        return ('%s.%s' % (module, field_name), [], {})
    