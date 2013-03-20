from django.db.models.fields.related import SingleRelatedObjectDescriptor
from django.db.models.query import QuerySet



# see http://jeffelmore.org/tag/django-python-inheritance-downcasting-orm-polymorphism-queryset/
class InheritanceQuerySet(QuerySet):

    def select_subclasses(self, *subclasses):
        if not subclasses:
            subclasses = [o for o in dir(self.model)
                          if isinstance(getattr(self.model, o), SingleRelatedObjectDescriptor)\
                          and issubclass(getattr(self.model,o).related.model, self.model)]

        new_qs = self.select_related(*subclasses)
        new_qs.subclasses = subclasses
        return new_qs


    def filter(self, *args, **kwargs): #@ReservedAssignment inherited method, can't rename
        qs = QuerySet.filter(self, *args, **kwargs)
        return qs.select_subclasses()

    def _clone(self, klass=None, setup=False, **kwargs):
        try:
            kwargs.update({'subclasses': self.subclasses})
        except AttributeError:
            pass
        return super(InheritanceQuerySet, self)._clone(klass, setup, **kwargs)
        
    def iterator(self):
        iterat = super(InheritanceQuerySet, self).iterator()
        if hasattr(self, 'subclasses'):
            for obj in iterat:
                for subclass in self.subclasses:
                    if hasattr(obj, subclass):
                       downcast_obj = getattr(obj, subclass)
                       break
       		else:
                    downcast_obj = obj
 
                yield downcast_obj
        else:
            for obj in iterat:
                yield obj
                
                
