# Give an example of variation of determine_progress1 that can be used to implement the logic for the function 
# that does not use if-statements. 
# Name: Jenny Soukhaseum
# Date: 10/01/2025

def determine_progress2(hits, spins):
    progress_messages = [
        "Get going!",       # index 0
        "On your way!",     # index 1
        "Almost there!",    # index 2
        "You win!"          # index 3
    ]

    hits_spins_ratio = hits / spins if spins != 0 else -1

    index = (
        0 if hits_spins_ratio <= 0 else
        1 + (hits_spins_ratio >= 0.25) + (hits_spins_ratio >= 0.5 and hits < spins)
    )

    return progress_messages[index]


    


