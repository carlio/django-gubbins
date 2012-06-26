from django.db import models
from gubbins.db.queryset import InheritanceQuerySet

                
class InheritanceManager(models.Manager):
    def get_query_set(self):
        return InheritanceQuerySet(model=self.model, using=self._db)
    
    def get(self, *args, **kwargs):
        qs = models.Manager.get(self, *args, **kwargs)
        return qs.select_subclasses()
    
    def filter(self, *args, **kwargs): #@ReservedAssignment : inherited method, can't rename
        return models.Manager.filter(self, *args, **kwargs).select_subclasses()
    
    def all(self): #@ReservedAssignment : inherited method, can't rename
        return models.Manager.all(self).select_subclasses()
