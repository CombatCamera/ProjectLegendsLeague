
from python.calculations.plate_appearances import calculate_plate_appearances
from python.calculations.strikeout_metrics import calculate_strikeout_tendency


def calculate_1911_al_hbp_total(batting_data):
    al_1911_batting = batting_data[
        (batting_data["lgID"] == "AL")
        & (batting_data["yearID"] == 1911)
    ]

    total_hbp = al_1911_batting["HBP"].sum()

    print("\n1911 AL reconstructed HBP total:")
    print(f"Total HBP: {total_hbp}")

    print("\n--------------------------------\n")

    return total_hbp

def calculate_1911_al_strikeout_tendency(batting_data):
    al_1911_batting = batting_data[
        (batting_data["lgID"] == "AL")
        & (batting_data["yearID"] == 1911)
        & (batting_data["playerID"] != "cobbty01")
        
    ]

    total_strikeouts = al_1911_batting["SO"].sum()
    
    total_plate_appearances = calculate_plate_appearances(
        al_1911_batting["AB"].sum(),
        al_1911_batting["BB"].sum(),
        al_1911_batting["HBP"].sum(),
        al_1911_batting["SH"].sum()
    )

    al_strikeout_tendency = calculate_strikeout_tendency(
        total_strikeouts, 
        total_plate_appearances
    ) * 100

    print("\n1911 AL Strikeout Tendency Calculation:")
    print(f"Total Strikeouts: {total_strikeouts}")
    print(f"Total Plate Appearances: {total_plate_appearances}")
    print(f"Strikeout Tendency: {al_strikeout_tendency:.2f}%")
    
    return al_strikeout_tendency


