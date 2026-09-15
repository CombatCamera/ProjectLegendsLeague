
def calculate_strikeout_tendency(strikeouts, plate_appearances):

    if plate_appearances == 0:
        return 0.0
    return (strikeouts / plate_appearances)