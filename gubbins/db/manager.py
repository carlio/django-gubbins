from django.db import models
from gubbins.db.queryset import InheritanceQuerySet

                
class InheritanceManager(models.Manager):
    def get_query_set(self):
        return InheritanceQuerySet(model=self.model, using=self._db)
    