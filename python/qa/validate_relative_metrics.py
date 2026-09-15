
from python.helpers.relative_metrics import relative_rate, relative_avoidance


def validate_relative_avoidance():
    
    test_cases = [
        (5, 10, 50.0),
        (10, 10, 0.0),
        (15, 10, -50.0),
        
    ]
    
    print(" ")
    print("---------------------------------")
    print(" ")

    for value, comparison_value, expected_relative_avoidance in test_cases:
        
        relative_ratio = relative_rate(value, comparison_value)
        test_relative_avoidance = relative_avoidance(relative_ratio)
        
        print(f"Test Relative Avoidance: {test_relative_avoidance}")
        print(f"Expected Relative Avoidance: {expected_relative_avoidance}")
        
        if test_relative_avoidance == expected_relative_avoidance:
            print("PASS: Relative avoidance function is working correctly.")
        else:
            print("FAIL: Relative avoidance function is not working correctly.")

        print(" ")