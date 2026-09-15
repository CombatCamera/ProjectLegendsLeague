from python.calculations.plate_appearances import calculate_plate_appearances
from python.calculations.strikeout_metrics import calculate_strikeout_tendency
from python.helpers.relative_metrics import relative_rate, relative_avoidance

def calculate_cobb_1911_plate_appearances(batting_data):
    ty_cobb_1911_batting = batting_data[
        (batting_data["playerID"] == "cobbty01")
        & (batting_data["yearID"] == 1911)
    ]
    
    plate_appearances = calculate_plate_appearances(
        ty_cobb_1911_batting["AB"].sum(),
        ty_cobb_1911_batting["BB"].sum(),
        ty_cobb_1911_batting["HBP"].sum(),
        ty_cobb_1911_batting["SH"].sum()
    )
    
    print("\nTy Cobb 1911 Plate Appearance Calculation:")
    print(f"Calculated Plate Appearances: {plate_appearances}")
    
    return plate_appearances
    
    
def calculate_cobb_1911_strikeout_tendency(
    batting_data, 
    plate_appearances
):
    ty_cobb_1911_batting = batting_data[
        (batting_data["playerID"] == "cobbty01")
        & (batting_data["yearID"] == 1911)
    ]
    
    strikeouts = ty_cobb_1911_batting["SO"].sum()
    
    cobb_strikeout_tendency = (
        calculate_strikeout_tendency(strikeouts, plate_appearances)
    ) * 100
    
    
    print("\nTy Cobb 1911 Strikeout Tendency Calculation:")
    print(f"Calculated Strikeouts: {strikeouts}")
    print(f"Strikeout Tendency: {cobb_strikeout_tendency:.2f}%")

    return cobb_strikeout_tendency


def calculate_cobb_strikeout_avoidance(
    cobb_strikeout_tendency, 
    al_strikeout_tendency
):
    
    relative_ratio = relative_rate(
        cobb_strikeout_tendency, 
        al_strikeout_tendency
    )
    
    cobb_relative_strikeout_avoidance = relative_avoidance(
        relative_ratio
    )
    print(" ")
    print("---------------------------------")
    print(" ")
    
    print(f"Relative Rate: {relative_ratio:.2f}")
    print(f"Ty Cobb's Relative Strikeout Avoidance: {cobb_relative_strikeout_avoidance:.2f}")
    
    return cobb_relative_strikeout_avoidance
