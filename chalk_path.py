def PATH(SQUARE_SIZE):
    PATH = [(),(4,331)]
    for i in range(2,7):  #upto square 6
        PATH.append((PATH[i-1][0] + SQUARE_SIZE,PATH[i-1][1]))
    PATH.append((PATH[6][0] + SQUARE_SIZE,PATH[6][1] - SQUARE_SIZE))
    for i in range(8,13):  #upto square 12
        PATH.append((PATH[i-1][0],PATH[i-1][1] - SQUARE_SIZE))
    PATH.append((PATH[12][0] + SQUARE_SIZE,PATH[12][1]))
    PATH.append((PATH[13][0] + SQUARE_SIZE,PATH[13][1]))
    for i in range(15,20): #upto square 19
        PATH.append((PATH[i-1][0],PATH[i-1][1] + SQUARE_SIZE))
    PATH.append((PATH[19][0] + SQUARE_SIZE,PATH[19][1] + SQUARE_SIZE))
    for i in range(21,26): #upto square 25
        PATH.append((PATH[i-1][0] + SQUARE_SIZE,PATH[i-1][1]))
    PATH.append((PATH[25][0],PATH[25][1] + SQUARE_SIZE))
    PATH.append((PATH[26][0],PATH[26][1] + SQUARE_SIZE))
    for i in range(28,33): #upto square 32
        PATH.append((PATH[i-1][0] - SQUARE_SIZE,PATH[i-1][1]))
    PATH.append((PATH[32][0] - SQUARE_SIZE,PATH[32][1] + SQUARE_SIZE))
    for i in range(34,39): #upto square 38
        PATH.append((PATH[i-1][0],PATH[i-1][1] + SQUARE_SIZE))
    PATH.append((PATH[38][0] - SQUARE_SIZE,PATH[38][1]))
    PATH.append((PATH[39][0] - SQUARE_SIZE,PATH[39][1]))
    for i in range(41,46): #upto square 45
        PATH.append((PATH[i-1][0],PATH[i-1][1] - SQUARE_SIZE))
    PATH.append((PATH[45][0] - SQUARE_SIZE,PATH[45][1] - SQUARE_SIZE))
    for i in range(47,52): #upto square 51
        PATH.append((PATH[i-1][0] - SQUARE_SIZE,PATH[i-1][1]))
    PATH.append((PATH[51][0],PATH[51][1] - SQUARE_SIZE))
    # Now the home run path
    for i in range(53,59): #red
        PATH.append((PATH[i-1][0] + SQUARE_SIZE,PATH[i-1][1]))
    PATH.append((PATH[13][0],PATH[13][1] + SQUARE_SIZE))
    for i in range(60,65): #blue
        PATH.append((PATH[i-1][0],PATH[i-1][1] + SQUARE_SIZE))
    PATH.append((PATH[26][0] - SQUARE_SIZE,PATH[26][1]))
    for i in range(66,71): #yellow
        PATH.append((PATH[i-1][0] - SQUARE_SIZE,PATH[i-1][1]))
    PATH.append((PATH[39][0],PATH[39][1] - SQUARE_SIZE))
    for i in range(72,77): #green
        PATH.append((PATH[i-1][0],PATH[i-1][1] - SQUARE_SIZE))
    return PATH
