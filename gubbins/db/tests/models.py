from gubbins.db.field import EnumField
from django.db import models



class TestField(EnumField):
    APPLE = 'a'
    PEAR = 'p'
    BANANA = 'b'
    
        
class TestModel(models.Model):
    fruit = TestField()