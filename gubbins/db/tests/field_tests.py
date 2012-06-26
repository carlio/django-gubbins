from django.test import TestCase
from gubbins.db.field import EnumField


class TestField(EnumField):
    APPLE = 'a'
    PEAR = 'p'
    BANANA = 'b'


class EnumFieldTest(TestCase):
    
    def test_options_constructor_arg(self):
        
        field = EnumField(options=['APPLE', 'PEAR', 'BANANA'])
        
        self.assertEqual('APPLE', field.APPLE)
        self.assertEqual('PEAR', field.PEAR)
        self.assertEqual('BANANA', field.BANANA)

        choices = field.choices        
        self.assertEqual(3, len(choices))
        self.assertTrue( ('APPLE', 'APPLE') in choices )
        self.assertTrue( ('PEAR', 'PEAR') in choices )
        self.assertTrue( ('BANANA', 'BANANA') in choices )
        
        
    def test_attribute_options(self):
            
        field = TestField()
            
        self.assertEqual('a', field.APPLE)
        self.assertEqual('p', field.PEAR)
        self.assertEqual('b', field.BANANA)

        choices = field.choices        
        self.assertEqual(3, len(choices))
        self.assertTrue( ('a', 'APPLE') in choices )
        self.assertTrue( ('p', 'PEAR') in choices )
        self.assertTrue( ('b', 'BANANA') in choices )
        

    def test_field_definition(self):
        
        field = TestField()
        self.assertEqual(1, field.max_length)
        
        field = EnumField(options=['APPLE', 'PEAR', 'BANANA'])
        self.assertEqual(6, field.max_length)
        