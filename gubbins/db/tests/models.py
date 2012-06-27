from gubbins.db.field import EnumField
from django.db import models
from gubbins.db.manager import InheritanceManager


# ---------------------
# EnumField test models
# ---------------------

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
    
    
    
# --------------------------------    
# Inheritence Queryset test models
# --------------------------------

class Colour(EnumField):
    RED = 'r'
    GREEN = 'gr'
    BLUE = 'bl'

class Vehicle(models.Model):
    objects = InheritanceManager()
    
    colour = Colour()
    wheel_count = models.IntegerField()

class Car(Vehicle):
    airbags = models.BooleanField()

class Train(Vehicle):
    train_number = models.CharField(max_length=10)