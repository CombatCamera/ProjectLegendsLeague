from python.qa.validate_relative_metrics import validate_relative_avoidance
from python.qa.validate_plate_appearances import validate_plate_appearances
from python.qa.validate_strikeout_metrics import validate_strikeout_tendency




def main():
    
    validate_relative_avoidance()
    validate_plate_appearances()
    validate_strikeout_tendency()
    
    
if __name__ == "__main__":
    main()