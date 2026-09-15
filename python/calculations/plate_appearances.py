def calculate_plate_appearances(AB, BB, HBP, SH, SF = 0):
    
    plate_appearances = AB + BB + HBP + SH + SF
    
    return plate_appearances