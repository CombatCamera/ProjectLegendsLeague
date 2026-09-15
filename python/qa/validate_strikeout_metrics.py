from python.calculations.strikeout_metrics import calculate_strikeout_tendency



def validate_strikeout_tendency():
    
    strikeouts = 42
    plate_appearances = 654
    
    calculated_tendency = calculate_strikeout_tendency(
        strikeouts,
        plate_appearances
    )
    
    rounded_tendency = round(calculated_tendency, 4)
    
    if rounded_tendency == 0.0642:
        print("Strikeout Tendency Validation Passed.")
        print(f"Calculated Strikeout Tendency: {rounded_tendency}")
    else:
        print("Strikeout Tendency Validation Failed.")
        print(f"Expected: 0.0642, Got: {rounded_tendency}")