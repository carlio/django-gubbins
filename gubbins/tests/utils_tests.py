import unittest
from gubbins.utils import append_params


class UtilsTest(unittest.TestCase):
    
    def test_append_params(self):
        url = 'http://www.fish.com/dir/page.html'
        url = append_params(url, {'a': 1, 'b': 'a i'})
        expected = 'http://www.fish.com/dir/page.html?a=1&b=a+i'
        self.assertEqual(expected, url)
        
    def test_append_params_with_existing(self):
        url = 'http://www.fish.com/dir/page.html?a=b'
        url = append_params(url, {'u': 1234})
        expected = 'http://www.fish.com/dir/page.html?a=b&u=1234'
        self.assertEqual(expected, url)
        
        
    