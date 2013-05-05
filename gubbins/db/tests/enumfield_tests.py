from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.test import TestCase
from gubbins.db.field import EnumField


# ------------------------
# Test cases
# ------------------------

class EnumFieldTest(TestCase):
    
    def test_static_choices_access(self):
        choices = FruitField.choices
        self.assertEqual(3, len(choices))
        self.assertTrue( ('a', 'APPLE') in choices )
        self.assertTrue( ('p', 'PEAR') in choices )
        self.assertTrue( ('b', 'BANANA') in choices )
        
    def test_options_from_attributes(self):
            
        field = FruitField()
            
        self.assertEqual('a', field.APPLE)
        self.assertEqual('p', field.PEAR)
        self.assertEqual('b', field.BANANA)

        choices = field.choices        
        self.assertEqual(3, len(choices))
        self.assertTrue( ('a', 'APPLE') in choices )
        self.assertTrue( ('p', 'PEAR') in choices )
        self.assertTrue( ('b', 'BANANA') in choices )
        

    def test_non_string_values(self):
        CountingModel.objects.create(count=CountingField.TWO)

    def test_values(self):
        field = FruitField()
        self.assertEqual(3, len(field.values))
        self.assertTrue(FruitField.APPLE in field.values)
        self.assertTrue(FruitField.PEAR in field.values)
        self.assertTrue(FruitField.BANANA in field.values)

    def test_max_length_calculation(self):
        
        field = FruitField()
        self.assertEqual(1, field.max_length)
        
        field = FishField()
        self.assertEqual(6, field.max_length)
        
        
    def test_custom_max_length_value(self):
        self.assertRaises(ImproperlyConfigured, FishField, max_length=2)
        FishField(max_length=200)
        
    def test_choices_kwarg_cannot_be_set(self):
        self.assertRaises(ImproperlyConfigured, FishField, choices=[('c', 'CAKES')])


    def test_from_string(self):
        self.assertTrue(FishField.is_valid_value('salmon'))
        self.assertFalse(FishField.is_valid_value('apple'))


class EnumFieldOnModelTest(TestCase):
    
    def test_value_persistence(self):
        test_model = FoodModel.objects.create(fruit=FruitField.APPLE)
        self.assertEqual(FruitField.APPLE, test_model.fruit)
        
        loaded_test_model = FoodModel.objects.get(pk=test_model.id)
        self.assertEqual(FruitField.APPLE, loaded_test_model.fruit)
        
    def test_default_value(self):
        food = FoodModel.objects.create(fruit=FruitField.APPLE)
        self.assertEqual(FishField.COD, food.fish)

    def test_only_valid_values_can_be_set(self):
        # test invalid valies
        self.assertRaises(ValueError, FoodModel.objects.create, fruit='chocolate')
        # check valid values
        FoodModel.objects.create(fruit=FruitField.APPLE, other_fruit=None)


class EnumSouthTest(TestCase):

    def test_correct_triple(self):

        field = FruitField(default=FruitField.APPLE)
        name, args, kwargs = field.south_field_triple()

        expected_kwargs = {'max_length': '1',
                           'default': "'a'"}

        self.assertEqual('gubbins.db.tests.enumfield_tests.FruitField', name)
        self.assertTrue( len(args) == 0 )
        self.assertEqual(expected_kwargs, kwargs)

        


# ---------------------
# Test models
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
