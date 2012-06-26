from django.db import models
import re
from django.core.exceptions import ImproperlyConfigured

class EnumField(models.CharField):

    """
    
    The following are identical::
    
      class SourceType(EnumField):
          options = ['WIKIPEDIA', 'BBC_NEWS', 'TWITTER']
          
      class SourceType(EnumField):
          WIKIPEDIA = 'w'
          BBC_NEWS = 'b'
          TWITTER = 't'
    
    """
    
    def __init__(self, options=None, *args, **kwargs):
        self._options = options
        kwargs = self._get_field_kwargs(kwargs)
        super(EnumField, self).__init__(*args, **kwargs)
    
    def __getattr__(self, name):
        if self._options is not None and name in self._options:
            return name
        raise AttributeError('No such enum option: %s' % name)
    
    def _get_field_kwargs(self, kwargs):
        options = self.options
        
        max_length = max( map(len, [getattr(self, attr_name) for attr_name in options]) )
        if 'max_length' in kwargs:
            if kwargs['max_length'] < max_length:
                raise ImproperlyConfigured('Supplied max_length is too short, enum values will be truncated! It should be %s or unspecified to be set automatically' % max_length)
        else:
            kwargs['max_length'] = max_length
        
        if 'choices' in kwargs:
            raise ImproperlyConfigured('"choices" keyword argument is not used as it is automatically generated')
        kwargs['choices'] = self.choices
        
        return kwargs
    
    @property
    def choices(self):
        return [ (getattr(self, attr_name), attr_name) for attr_name in self.options ]

    @property
    def options(self):
        """
        Gets the list of possible options for this object.
        """
        # first check in case they are explicitly defined
        if self._options is not None:
            return self._options
        
        options = []
        
        for attr_name in dir(self):
            if attr_name.startswith('_'):
                # ignore any 'private' attributes
                continue
            if not re.match('^[A-Z][A-Z0-9_]+$', attr_name):
                # ignore anything which is not all uppercase
                continue
            attr = getattr(self, attr_name)
            if callable(attr):
                # ignore anything which is not a simple value
                continue
            options.append(attr_name)
        
        return options
            
