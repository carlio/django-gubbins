from django.conf.urls import include


class ReusableAppURLs(object):
    
    def __init__(self, app_namespace, urlpatterns):
        self.app_namespace = app_namespace
        self.urlpatterns = urlpatterns

    def __call__(self, instance_namespace=None):
        instance_namespace = instance_namespace or self.app_namespace
        return include(self.urlpatterns, self.app_namespace, instance_namespace)
  
    