# -*- coding: UTF-8 -*-

from django.test import TestCase
from gubbins.db.field import JSONField
from django.db import models

# -------------------
# Test cases
# -------------------


class JSONFieldTest(TestCase):
    
    def _test_storable(self, data):
        something = SomethingModel.objects.create(blob=data)
        something2 = SomethingModel.objects.get(pk=something.id)       
        self.assertEqual(data, something2.blob)
        
    
    def test_store_dict(self):
        """
        Ensures that the JSONField can store and correctly
        retrieve a dictionary with a variety of data types
        as values
        """
        data = {'a': 1, 'b': 'two', 'c': u'\xfc\xe9\xdf\xa2\u03a9', 'd': [1,2,3,4], 
                'e': {'e1': 4, 'e2': 'fish'} }
        self._test_storable(data)
        

    def test_store_list(self):
        """
        Ensures that the JSONField can store a list directly
        """
        array = [1,2,3,'a','b',{'c':4, 'e':['t', 'y']}]
        self._test_storable(array)

    def test_store_unknown_types(self):
        class Banana:
            pass
        self.assertRaises(JSONField.CannotStoreTypeException, self._test_storable, set())
        self.assertRaises(JSONField.CannotStoreTypeException, self._test_storable, Banana())
        self.assertRaises(JSONField.CannotStoreTypeException, self._test_storable, 'fish')




class JSONSouthTest(TestCase):

    def test_correct_triple(self):

        field = JSONField()
        name, args, kwargs = field.south_field_triple()


        self.assertEqual('gubbins.db.field.JSONField', name)
        self.assertTrue( len(args) == 0 )

        print name, args, kwargs

# -------------------
# Test models
# -------------------

class SomethingModel(models.Model):
    blob = JSONField()
