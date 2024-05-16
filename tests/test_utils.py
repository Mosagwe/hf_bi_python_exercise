import unittest
from utils.utils import time_to_minutes, min_distance_to_chili

class TestUtils(unittest.TestCase):
    def test_time_to_minutes_hours_and_minutes(self):
        self.assertEqual(time_to_minutes("1H30M"), 90)

    def test_time_to_minutes_only_minutes(self):
        self.assertEqual(time_to_minutes("45M"), 45)

    def test_time_to_minutes_empty_string(self):
        self.assertEqual(time_to_minutes(""), 0)

    def test_min_distance_to_chili(self):
        ingredient_list = "1 cup of chilies"
        self.assertEqual(min_distance_to_chili(ingredient_list), 0)

        ingredient_list = "1 cup of water"
        self.assertTrue(min_distance_to_chili(ingredient_list) > 0)

if __name__ == '__main__':
    unittest.main()