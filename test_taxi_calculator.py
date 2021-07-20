import unittest
from taxi_calculator import FareCalculator

class TestTaxiCalculator(unittest.TestCase):
    def test_validate_format(self):
        calculator = FareCalculator() # construct new object for new test to refresh state for each test
        # Expected
        self.assertTrue(calculator.__validate_format__([
            "00:00:00.000 0.0",
            "00:01:00.125 441.2", 
            "00:02:00.125 1141.2",
            "00:03:00.100 1800.8",
        ]))
        # Data less than 2 row
        self.assertFalse(calculator.__validate_format__([
            "00:00:00.000 0.0",
        ]))
        # Data doesn't match with expected format 
        self.assertFalse(calculator.__validate_format__([
            "00:00:00.000 0.0",
            "00:01:00.125Z441.2", 
            "00:02:00.125 1141.2",
            "00:03:00.100 1800.8",
        ]))
        # Data contain blank line
        self.assertFalse(calculator.__validate_format__([
            "00:00:00.000 0.0",
            "00:01:00.125 441.2", 
            "",
            "00:03:00.100 1800.8",
        ]))

    def test_validate_time(self):
        calculator = FareCalculator() # construct new object for new test to refresh state for each test
        # expected
        self.assertTrue(calculator.__validate_time_step__([
            "00:00:00.000",
            "00:01:00.125", 
            "00:02:00.125",
            "00:03:00.100",
        ]))
        # Past time appear
        self.assertFalse(calculator.__validate_time_step__([
            "00:00:00.000",
            "00:01:00.125", 
            "00:02:00.125",
            "00:01:00.125",
        ]))
        # Time interval more than 5 minutes
        self.assertFalse(calculator.__validate_time_interval__([
            "00:00:00.000",
            "00:01:00.125", 
            "00:08:00.125",
            "00:09:00.125",
        ]))

    def test_validate_milage(self):
        calculator = FareCalculator() # construct new object for new test to refresh state for each test
        #expected
        self.assertTrue(calculator.__validate_mileage__([
            0.0,
            441.2, 
            1141.2,
            1800.8,
        ]))
        # Data zero total mileage
        self.assertFalse(calculator.__validate_mileage__([
            0.0,
            0.0,
        ]))

    def test_get_time_list(self):
        calculator = FareCalculator() # construct new object for new test to refresh state for each test
        # expected 
        self.assertEqual(calculator.__get_time_list__([
            "00:00:00.000 0.0",
            "00:01:00.125 441.2", 
            "00:02:00.125 1141.2",
            "00:03:00.100 1800.8",
        ]), [
            "00:00:00.000",
            "00:01:00.125", 
            "00:02:00.125",
            "00:03:00.100",
        ])
         # unexpected 
        self.assertNotEqual(calculator.__get_time_list__([
            "00:00:00.000T0.0",
            "00:01:00.125 441.2", 
            "00:02:00.125 1141.2",
            "00:03:00.100 1800.8",
        ]), [
            "00:00:00.000",
            "00:01:00.125", 
            "00:02:00.125",
            "00:03:00.100",
        ])
    
    def test_get_mileage(self):
        calculator = FareCalculator() # construct new object for new test to refresh state for each test
        # expected
        self.assertEqual(calculator.__get_mileage_list__(
            [
            "00:00:00.000 0.0",
            "00:01:00.125 441.2", 
            "00:02:00.125 1141.2",
            "00:03:00.100 1800.8",
        ]), [
            0.0,
            441.2, 
            1141.2,
            1800.8,
        ])

    def test_fare_adjuster(self):
        calculator = FareCalculator() # construct new object for new test to refresh state for each test
        # below 1 Km use 400 yen
        self.assertEqual(calculator.fare_adjuster(100.0), 400)
        # below 1 Km use 400 yen
        self.assertEqual(calculator.fare_adjuster(800.0), 400)
        # above 1 Km below 10.000 Km use add 40 yen for every 400 m
        self.assertEqual(calculator.fare_adjuster(1141.0), 400)
        # above 1 Km below 10.000 Km use add 40 yen for every 400 m
        self.assertEqual(calculator.fare_adjuster(1441.0), 400)
        # above 1 Km below 10.000 Km use add 40 yen for every 400 m
        self.assertEqual(calculator.fare_adjuster(1841.0), 440)