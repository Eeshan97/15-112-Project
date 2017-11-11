#    15-112: Principles of Programming and Computer Science
#    Project: AI based Ludo
#    Name      : Swapnendu Sanyal
#    AndrewID  : swapnens

#    File Created: November 6, 2017
#    Modification History:
#    Start             End
#    27/10 14:30       27/10 20:00
#    30/10 21:05       19/10 22:08
########################## IMPORTING AND INITIALIZING ALL THE LIBRARIES ###############################
import pygame
pygame.init()
import time
import random
#######################################################################################################

############################## CONSTANTS ##############################################################
DISPLAY_HEIGHT = 750
DISPLAY_WIDTH = 700
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
SQUARE_SIZE = 705/15 #side of the image by number of boxes
COIN_RADIUS = SQUARE_SIZE/4
gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))
pygame.display.set_caption('LUDO - Main Menu')
image = pygame.image.load('ludo.jpg')
pygame.display.set_icon(image)
clock = pygame.time.Clock()
FPS = 15
medfont = pygame.font.SysFont("comicsansms",50)
SAFE_ZONE = [2,15,28,40]  # Pawns cannot be captured here
RED_ROAD = [53,54,55,56,57,58]
BLUE_ROAD = [59,60,61,62,63,64]
YELLOW_ROAD = [65,66,67,68,69,70]
GREEN_ROAD = [71,72,73,74,75,76]
IS_COIN_PRESENT = [False] * 53 # to chack if any coin is present at a square
################## CHALKING OUT THE PATH ################
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
#######################################################################################################
def roll():  #rolling the dice
    return random.choice([1,2,3,4,5,6])

# this brings back the coins back to the original position
# this function also empties the path
def game_initialize():
    IS_COIN_PRESENT = [False] * 53 # to check if any coin is present at a square
    position = {'red':[None],'blue':[None],'yellow':[None],'green':[None]}
    #RED COINS
    for i in [(PATH[4][0],PATH[10][1]),(PATH[4][0],PATH[8][1]),(PATH[3][0],PATH[9][1]),(PATH[5][0],PATH[9][1])]:
        position['red'].append(i)
    #BLUE COINS
    for i in [(PATH[23][0],PATH[18][1]),(PATH[23][0],PATH[16][1]),(PATH[22][0],PATH[17][1]),(PATH[24][0],PATH[17][1])]:
        position['blue'].append(i)
    #YELLOW COINS
    for i in [(PATH[23][0],PATH[35][1]),(PATH[23][0],PATH[37][1]),(PATH[22][0],PATH[36][1]),(PATH[24][0],PATH[36][1])]:
        position['yellow'].append(i)
    #GREEN COINS
    for i in [(PATH[4][0],PATH[43][1]),(PATH[4][0],PATH[41][1]),(PATH[3][0],PATH[42][1]),(PATH[5][0],PATH[42][1])]:
        position['green'].append(i)
    return position

def drawcoins(position): #to draw coints on the board
    for i in position:
        if i == 'red':
            color = RED
        elif i == 'blue':
            color = BLUE
        elif i == 'green':
            color = GREEN
        else:
            color = YELLOW
        for j in position[i]:
            if j != None:
                pygame.draw.circle(gameDisplay,BLACK,j,COIN_RADIUS,5)
                #above one gives a black boder
                #next one fills it with color
                pygame.draw.circle(gameDisplay,color,j,COIN_RADIUS - 5,0)


def distance(point1,point2): # to calculate distance between 2 points
    x1 = point1[0]*1.0
    x2 = point2[0]
    y1 = point1[1]
    y2 = point2[1]
    return (x1-x2)**2 + (y1-y2)**2

def detect_coin(click,position): #to detect which coin was selected
    coin_selected = []
    for i in position:
                for j in range(1,len(position[i])):
                    if (distance(click,position[i][j]) <= COIN_RADIUS**2):
                        coin_selected.append((i,j))
    return coin_selected
def detect_square_number(PATH,coin):
    for i in range(1,len(PATH)):
        if PATH[i] == coin:
            return i
    return -1
def coin_move(position,coin_selected,move):
        color = coin_selected[0][0]
        coin_number = coin_selected[0][1]
        print 'here',color,coin_number,move
        temp = detect_square_number(PATH,position[color][coin_number])
        if temp == -1:
            if color == 'red':
              position[color][coin_number] = PATH[2]
            elif color == 'blue':
               position[color][coin_number] = PATH[15]
            elif color == 'green':
                position[color][coin_number] = PATH[41]
            else:
                position[color][coin_number] = PATH[28]
        #position[color][coin_number] = PATH[ + move]

def gameloop():
    gameOver = False
    gameExit = False
    while not gameExit:
        #if gameOver == True: ##########come back later - replay options
            #pass

        coin_position = game_initialize()
        while not gameOver:
            gameDisplay.blit(image,(0,45))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = gameExit = True
                if event.type == pygame.MOUSEBUTTONUP:
                    #print pygame.mouse.get_pos()
                    coin_selected = detect_coin(pygame.mouse.get_pos(),coin_position)
                    if coin_selected:
                        move = roll()
                        #print move,coin_selected,coin_position
                        coin_move(coin_position,coin_selected,move)
            drawcoins(coin_position)
            pygame.display.update()
            clock.tick(FPS)

############################# GAME EXIT ###############################################################
gameloop()
pygame.quit()
exit()

################################ CITATIONS ############################################################

# Main Menu Image = <https://www.codester.com/static/uploads/items/3366/icon.png>
