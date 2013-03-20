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
                    # note: slightly funky behaviour here - for Django <= 1.4, the parent class has an attribute
                    # for every subclass which is None; for Django >= 1.5, trying to access that will throw an
                    # exception. Therefore for compatability with both versions, we use 'hasattr' to see if the
                    # the attribute exists (will be False for 1.5+), but then also test the value we get in case
                    # it is None (hasattr is true for <=1.4, and will return None)
                    if hasattr(obj, subclass):
                        downcast_obj = getattr(obj, subclass)
                        if downcast_obj is not None:
                            break
       		else:
                    downcast_obj = obj
 
                yield downcast_obj
        else:
            for obj in iterat:
                yield obj
                
                
