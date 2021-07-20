from taxi_calculator import FareCalculator

if __name__ == "__main__":
    # Run code example
    example = [
        {
            "example": [
            "00:00:00.000 0.0", 
            "00:01:00.125 441.2",
            "00:02:00.125 1141.2",
            "00:03:00.100 1800.8",
            "00:04:00.100 2500.8",
            "00:05:00.100 3200.8",
            "00:06:00.100 3900.8",
            "00:07:00.100 4600.8",
            "00:08:00.100 5300.8",
            "00:08:00.100 6000.8",
            "00:09:00.100 6700.8",
            "00:10:00.100 7400.8",
            "00:11:00.100 8100.8",
            "00:12:00.100 8800.8",
            "00:13:00.100 9500.8",
            "00:14:00.100 10200.8",
            "00:15:00.100 10900.8",
        ],
        "expected": 1080
        }
    ]

    calculator = FareCalculator()
    for ex in example:
        calculation_result = calculator.calculate_fare(ex['example'])
        print(calculation_result)