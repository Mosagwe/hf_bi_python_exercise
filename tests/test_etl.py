import unittest
from unittest.mock import patch, mock_open
import os
from utils.etl import download_json, format_json, process_data

import json


class TestDownload(unittest.TestCase):
    @patch('utils.etl.requests.get')
    def test_download_json_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b'{"key": "value"}'

        test_filename = 'test_file.json'
        download_json('http://example.com', test_filename)

        self.assertTrue(os.path.exists(test_filename))
        with open(test_filename, 'rb') as f:
            content = f.read()
            self.assertEqual(content, b'{"key": "value"}')

        # Clean
        os.remove(test_filename)

    @patch('utils.etl.requests.get')
    def test_download_json_failure(self, mock_get):
        mock_get.return_value.status_code = 404

        with self.assertRaises(Exception):
            download_json('http://example.com', 'test_file.json')

    def setUp(self):
        # init config
        self.test_data = [
           {
                "name": "Easy Green Chile Enchiladas",
                "ingredients": "1 whole Onion, Diced\n2 Tablespoons Butter\n1 can (15 Ounce) Green Enchilada Sauce\n2 cans (4 Ounce) Chopped Green Chilies\n12 whole Corn Tortillas\n2 cups Freshly Grated Cheddar (or Cheddar-jack) Cheese (or Any Cheese You'd Like)\n Sour Cream\n Salsa\n Pico De Gallo (optional)\n Guacamole (optional)\n Cilantro Leaves, Optional",
                "url": "http://thepioneerwoman.com/cooking/2012/05/easy-green-chile-enchiladas/",
                "image": "http://static.thepioneerwoman.com/cooking/files/2012/05/enchilada.jpg",
                "cookTime": "PT10M",
                "recipeYield": "4",
                "datePublished": "2012-05-31",
                "prepTime": "PT5M",
                "description": "When I was in Albuquerque with Marlboro Man and the boys a month ago, I had a really fun book signing. Such incredibly nice a..."
            },
            {
                "name": "Recipe2",
                "ingredients": "2 cups water\n1 cup rice\nSalt to taste",
                "url": "http://example.com/recipe2",
                "image": "http://example.com/images/recipe2.jpg",
                "cookTime": "PT20M",
                "recipeYield": "2",
                "datePublished": "2021-02-01",
                "prepTime": "PT10M",
                "description": "An easy recipe for plain rice."
            }
        ]

        # Transform JSON to match with the JSON file downloaded
        self.json_test_data = '\n'.join(json.dumps(recipe) for recipe in self.test_data)


    def test_format_json(self):

        with patch('builtins.open', mock_open(read_data=self.json_test_data)) as mock_file:
            # 
            expected_data = self.test_data
            result = format_json('dummy_file.json')
            self.assertEqual(result, expected_data)
            mock_file.assert_called_once_with('dummy_file.json', 'r')


    @patch('utils.utils.time_to_minutes')
    @patch('utils.utils.min_distance_to_chili')
    @patch('utils.utils.calculate_difficulty')
    def test_process_data(self, mock_calculate_difficulty, mock_min_distance_to_chili, mock_time_to_minutes):

        with patch('builtins.open', mock_open(read_data=self.json_test_data)) as mock_file:

            # Config mocks
            mock_min_distance_to_chili.side_effect = lambda ingredient: 0 if "chilies" in ingredient else 2
            mock_time_to_minutes.side_effect = lambda x: 20 if "PT20M" in x else 30  # 
            mock_calculate_difficulty.side_effect = lambda row: "Easy" if row.get('total_time', 0) <= 30 else "Medium"

            filtered_recipes, average_times_filtered = process_data('dummy_file.json')          

            #verify
            self.assertEqual(len(filtered_recipes), 1)  # 
            self.assertEqual(filtered_recipes.iloc[0]['difficulty'], 'Medium')
            self.assertTrue('Medium' in average_times_filtered['difficulty'].values)


if __name__ == '__main__':
    unittest.main()