from python.calculations.plate_appearances import calculate_plate_appearances

def validate_plate_appearances():
    calculated_plate_appearances = calculate_plate_appearances(591, 44, 8, 11, 0)
    
    if calculated_plate_appearances == 654:
        print("Plate Appearance Validation Passed.")
        print(f"Calculated Plate Appearances: {calculated_plate_appearances}")
    else:
        print("Plate Appearance Validation Failed.")
        print(f"Expected: 654, Got: {calculated_plate_appearances}")