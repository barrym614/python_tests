import unittest

from weather_app.weather import fetch_current_weather


class TestWeather(unittest.TestCase):
    def test_sample_returns_expected_keys(self):
        data = fetch_current_weather(api_key="", city="Any")
        self.assertIn("city", data)
        self.assertIn("temp_c", data)
        self.assertIn("description", data)


if __name__ == "__main__":
    unittest.main()
