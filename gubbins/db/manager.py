from django.db import models
from gubbins.db.queryset import InheritanceQuerySet

                
class InheritanceManager(models.Manager):

    def all(self):
        return self.get_query_set().select_subclasses()

    def get_query_set(self):
        return InheritanceQuerySet(model=self.model, using=self._db)
    