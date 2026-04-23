import unittest
import json
from app import app

class TestYourFlaskApp(unittest.TestCase):
    """Simple tests for your Flask API"""
    
    def setUp(self):
        """Create test browser before each test"""
        self.client = app.test_client()
        self.client.testing = True

    def test_get_all_items(self):
        """Test GET /get-allItems returns 2 items"""
        response = self.client.get('/get-allItems')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(len(data['items']), 3)
        self.assertEqual(data['items'][0]['name'], 'Water Bottle')
        print("All items test PASSED")

    def test_add_coffee(self):
        """Test POST /add-items adds Coffee"""
        new_item = {"name": "Coffee", "price": 30}
        
        response = self.client.post('/add-items',
                                  data=json.dumps(new_item),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Items added')
        print("Add Coffee test PASSED")

    def test_get_cola(self):
        """Test GET /get-item?name=Cola"""
        response = self.client.get('/get-item?name=Cola')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Cola')
        self.assertEqual(data['price'], 25)
        print("Get Cola test PASSED")

    def test_add_bad_item(self):
        """Test POST missing price field"""
        bad_item = {"name": "Bad Item"}
        
        response = self.client.post('/add-items',
                                  data=json.dumps(bad_item),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        print("Error test PASSED")

      
    def test_item_not_found(self):
        """Test GET /get-item?name=Mixture"""
        response= self.client.get('/get-item?name=Mixture')
        self.assertEqual(response.status_code, 404)
        print("Not found test PASSED")

    def test_random_user(self):
        """Test GET /random-user"""
        response = self.client.get('/random-user')
        self.assertEqual(response.status_code, 200)
        print("Random user test PASSED")

    def test_add_item_invalid_price_type(self):
        """"Test POST with invalid price type (string instead of number)"""
        bad_item = {"name": "Tea", "price": "ten"}

        response = self.client.post('/add-iteams',
                                    data = json.dumps(bad_item),
                                    content_type='application/json')
        
    def test_duplicate_item(self):
        """Test POST adding duplicate item name"""
        duplicate_item = {"name": "cola", "price": 25}
        response = self.client.post('/add-items',
                                    data = json.dumps(duplicate_item),
                                    content_type = 'application/json')

if __name__ == '__main__':
    unittest.main(verbosity=2)
    