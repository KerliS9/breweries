import unittest
from unittest.mock import patch, MagicMock
from app.fetch_api import get_list_breweries  # Replace with actual import

class TestGetListBreweries(unittest.TestCase):
    @patch('app.fetch_api')  # Mock the fetch_api dependency
    def test_successful_multiple_pages(self, mock_fetch):
        # Setup mock to return different responses for different pages
        mock_fetch.side_effect = [
            [{'id': f'brewery_{i}'} for i in range(1, 201)],  # Page 1
            [{'id': f'brewery_{i}'} for i in range(201, 401)], # Page 2
            []  # Empty response to break loop
        ]
        
        # Call the function
        result = get_list_breweries()
        
        # Assertions
        self.assertEqual(len(result), 400)
        self.assertEqual(mock_fetch.call_count, 3)
        mock_fetch.assert_any_call(
            "https://api.openbrewerydb.org/v1/breweries",
            params={"page": 1, "per_page": 200}
        )
        mock_fetch.assert_any_call(
            "https://api.openbrewerydb.org/v1/breweries",
            params={"page": 2, "per_page": 200}
        )
    
    @patch('app.fetch_api')
    def test_single_page_response(self, mock_fetch):
        # Mock single page response
        mock_data = [{'id': f'brewery_{i}'} for i in range(1, 151)]
        mock_fetch.side_effect = [mock_data, []]
        
        result = get_list_breweries()
        
        self.assertEqual(len(result), 150)
        self.assertEqual(mock_fetch.call_count, 2)
    
    @patch('fetch_api')
    def test_empty_response_first_call(self, mock_fetch):
        # Mock empty first response
        mock_fetch.return_value = []
        
        result = get_list_breweries()
        
        self.assertEqual(len(result), 0)
        mock_fetch.assert_called_once()
    
    @patch('fetch_api')
    def test_api_error_handling(self, mock_fetch):
        # Mock API raising an exception
        mock_fetch.side_effect = Exception("API Connection Error")
        
        with self.assertRaises(Exception) as context:
            get_list_breweries()
            
        self.assertTrue("API Connection Error" in str(context.exception))
    
    @patch('fetch_api')
    @patch('builtins.print')
    def test_debug_print_output(self, mock_print, mock_fetch):
        # Mock data and verify print output
        mock_fetch.side_effect = [
            [{'id': 'brewery_1'}, {'id': 'brewery_2'}],
            []
        ]
        
        get_list_breweries()
        
        # Verify the debug print statement
        mock_print.assert_called_with('get_list_breweries:', 2)
    
    @patch('fetch_api')
    def test_pagination_logic(self, mock_fetch):
        # Verify pagination parameters are correct
        mock_fetch.side_effect = [
            [{'id': 'brewery_1'}],
            []
        ]
        
        get_list_breweries()
        
        # Check pagination params were incremented
        calls = mock_fetch.call_args_list
        self.assertEqual(calls[0][1]['params']['page'], 1)
        self.assertEqual(calls[1][1]['params']['page'], 2)
    
    @patch('fetch_api')
    def test_response_data_structure(self, mock_fetch):
        # Verify function handles different data structures
        mock_fetch.side_effect = [
            [{'id': '1', 'name': 'Test Brewery', 'city': 'Portland'}],
            []
        ]
        
        result = get_list_breweries()
        
        self.assertEqual(result[0]['name'], 'Test Brewery')
        self.assertEqual(result[0]['city'], 'Portland')

if __name__ == '__main__':
    unittest.main()