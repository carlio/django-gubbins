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
    

class CountingField(EnumField):
    ONE = 1
    TWO = 2
    THREE = 3
                
class FoodModel(models.Model):
    fruit = FruitField()
    fish = FishField(default=FishField.COD)
    other_fruit = FruitField(blank=True, null=True)
    
    
class CountingModel(models.Model):
    count = CountingField()
    
    
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