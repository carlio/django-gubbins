from django.db import models
import re

class EnumField(models.CharField):
    
    def get_options(self):
        """
        Gets the list of possible options for this object.
        """
        # first check in case they are explicitly defined
        if hasattr(self, 'options'):
            return self.options
        
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
            
