from gubbins.db.field import EnumField
from django.db import models



class FruitField(EnumField):
    APPLE = 'a'
    PEAR = 'p'
    BANANA = 'b'
    
    
class FishField(EnumField):
    SALMON = 'salmon'
    COD = 'cod'
    TROUT = 'trout'
        
        
class FoodModel(models.Model):
    fruit = FruitField()
    fish = FishField(default=FishField.COD)
    