from django.test import TestCase
from gubbins.db.tests.models import Car, Train, Colour, Vehicle

class TestModelInheritence(TestCase):
    
    def test_subclasses_returned_from_filter(self):
        
        _ = Car.objects.create(wheel_count=4, airbags=True, colour=Colour.RED)
        green_car = Car.objects.create(wheel_count=4, airbags=True, colour=Colour.GREEN)
        train = Train.objects.create(wheel_count=50, train_number='X312B', colour=Colour.GREEN)
        
        green_vehicles = Vehicle.objects.filter(colour=Colour.GREEN)
        
        self.assertEqual(2, green_vehicles.count())
        
        self.assertEqual(green_car.id, green_vehicles[0].id)
        self.assertTrue( isinstance(green_vehicles[0], Car) )
        
        self.assertEqual(train.id, green_vehicles[1].id)
        self.assertTrue( isinstance(green_vehicles[1], Train) )

    def test_subclasses_returned_from_get(self):
        car = Car.objects.create(wheel_count=4, airbags=True, colour=Colour.RED)
        fetched_car = Vehicle.objects.get(pk=car.id)
        self.assertTrue( isinstance( fetched_car, Car) )