from django.db import models
import re

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
    
    def _get_field_kwargs(self, kwargs):
        options = self.get_options()
        max_length = max( map(len, options) )
        kwargs.update( {'max_length': max_length, 
                        'choices': self.choices } )
        return kwargs
    
    @property
    def choices(self):
        options = self.options
        return zip( options, options )
    
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
            if attr_name.starts_with('_'):
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
            
