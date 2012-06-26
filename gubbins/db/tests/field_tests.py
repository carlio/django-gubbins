from django.test import TestCase
from gubbins.db.field import EnumField
from django.core.exceptions import ImproperlyConfigured


class TestField(EnumField):
    APPLE = 'a'
    PEAR = 'p'
    BANANA = 'b'


class EnumFieldTest(TestCase):
    
    def test_options_from_constructor_arg(self):
        
        field = EnumField(options=['APPLE', 'PEAR', 'BANANA'])
        
        self.assertEqual('APPLE', field.APPLE)
        self.assertEqual('PEAR', field.PEAR)
        self.assertEqual('BANANA', field.BANANA)

        choices = field.choices        
        self.assertEqual(3, len(choices))
        self.assertTrue( ('APPLE', 'APPLE') in choices )
        self.assertTrue( ('PEAR', 'PEAR') in choices )
        self.assertTrue( ('BANANA', 'BANANA') in choices )
        
        
    def test_options_from_attributes(self):
            
        field = TestField()
            
        self.assertEqual('a', field.APPLE)
        self.assertEqual('p', field.PEAR)
        self.assertEqual('b', field.BANANA)

        choices = field.choices        
        self.assertEqual(3, len(choices))
        self.assertTrue( ('a', 'APPLE') in choices )
        self.assertTrue( ('p', 'PEAR') in choices )
        self.assertTrue( ('b', 'BANANA') in choices )
        

    def test_max_length_calculation(self):
        
        field = TestField()
        self.assertEqual(1, field.max_length)
        
        field = EnumField(options=['APPLE', 'PEAR', 'BANANA'])
        self.assertEqual(6, field.max_length)
        
        
    def test_custom_max_length_value(self):
        self.assertRaises(ImproperlyConfigured, EnumField, options=['FISH'], max_length=2)
        EnumField(options=['FISH'], max_length=200)
        
    def test_choices_kwarg_cannot_be_set(self):
        self.assertRaises(ImproperlyConfigured, EnumField, options=['CAKES'], choices=[('c', 'CAKES')])
        
        
        
        