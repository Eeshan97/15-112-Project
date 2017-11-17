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
import chalk_path
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
FPS = 7
medfont = pygame.font.SysFont("comicsansms",50)
SAFE_ZONE = [2,15,28,40]  # Pawns cannot be captured here
RED_ROAD = [53,54,55,56,57,58]
BLUE_ROAD = [59,60,61,62,63,64]
YELLOW_ROAD = [65,66,67,68,69,70]
GREEN_ROAD = [71,72,73,74,75,76]
IS_COIN_PRESENT = [False] * 53 # to chack if any coin is present at a square
spritesheet = [] # to store the images of dice
for i in range(1,7):
    spritesheet.append(pygame.image.load('dice (' + str(i)+').png'))
print 'done loading'
#######################################################################################################
def roll():  #rolling the dice
    dice = random.choice([1,2,3,4,5,6])
    i = 0
    while i <12:
        pygame.draw.rect(gameDisplay,BLACK,(500,0,DISPLAY_WIDTH-500,50))
        gameDisplay.blit(spritesheet[i%6],(500,0))
        message_to_screen(color = WHITE, msg = str(i), where_text = (DISPLAY_WIDTH-100,22) )
        i += 1
        clock.tick(2*FPS)
        pygame.display.update()
    pygame.draw.rect(gameDisplay,BLACK,(500,0,DISPLAY_WIDTH-500,50))
    gameDisplay.blit(spritesheet[dice-1],(500,0))
    message_to_screen(color = WHITE, msg = str(dice), where_text = (DISPLAY_WIDTH-100,22) )
    return dice

# this brings back the coins back to the original position
# this function also empties the path
def game_initialize():
    PATH = chalk_path.PATH(SQUARE_SIZE)
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
    return (PATH,position)

def drawcoins(position,PATH): #to draw coints on the board
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
            if j != None and j not in [PATH[58],PATH[64],PATH[70],PATH[76]]:
                pygame.draw.circle(gameDisplay,BLACK,j,COIN_RADIUS,5)
                #above one gives a black boder
                #next one fills it with color
                pygame.draw.circle(gameDisplay,color,j,COIN_RADIUS - 5,0)


def distance(point1,point2): # to calculate distance between 2 points
    x1 = point1[0]
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
    return False

def is_valid_move(color,start,destination,position,PATH):
    for i in range(start+1,destination):
        for j in position:
            for k in position[j][1:]:
                if k == PATH[i]:
                    return False
    return True
'''def capture(color,destination,position PATH):
    for j in position:
        for k in position[j][1:]:
            pass'''

def coin_move(position,coin_selected,move,PATH):
        color = coin_selected[0][0]
        coin_number = coin_selected[0][1]
        move_made = True
        did_coin_start = detect_square_number(PATH,position[color][coin_number])
        if not did_coin_start:
            if move == 6:
                if color == 'red':
                  position[color][coin_number] = PATH[2]
                elif color == 'blue':
                   position[color][coin_number] = PATH[15]
                elif color == 'green':
                    position[color][coin_number] = PATH[41]
                else:
                    position[color][coin_number] = PATH[28]
        else:
            #if isvalid(did_coin_start,color,move):
            if color == 'blue' and 8<=did_coin_start<=13 and did_coin_start + move >13:
                change = move - (13 - did_coin_start)
                if is_valid_move(color,did_coin_start,13,position,PATH):
                    position['blue'][coin_number] = PATH[58+change]
                else: move_made = False
            elif color == 'green' and 34<=did_coin_start<=39 and did_coin_start + move >39:
                if is_valid_move(color,did_coin_start,39,position,PATH):
                    change = move - (39 - did_coin_start)
                    position['green'][coin_number] = PATH[70 +change]
                else: move_made = False
            elif color == 'yellow' and 21<=did_coin_start<=26 and did_coin_start + move >26:
                change = move - (26 - did_coin_start)
                if is_valid_move(color,did_coin_start,26,position,PATH):
                    position['yellow'][coin_number] = PATH[64+change]
                else: move_made = False
            elif color == 'red' and did_coin_start>52 and did_coin_start + move > 58:
                move_made = False
            elif color == 'green' and did_coin_start>=71 and did_coin_start + move > 76:
                move_made = False
            elif color == 'blue' and did_coin_start>=59 and did_coin_start + move > 64:
                move_made = False
            elif color == 'yellow' and did_coin_start>=65 and did_coin_start + move > 76:
                move_made = False
            elif color in ['green','blue','yellow'] and 58>=did_coin_start + move>52:
                position[color][coin_number] = PATH[did_coin_start+move-52]
            else:
                destination = (did_coin_start + move)
                if is_valid_move(color,did_coin_start,destination,position,PATH):
                    position[color][coin_number] = PATH[did_coin_start + move]
                else: move_made = False
        print color,coin_number,move
        if move_made: return position, roll(),move_made
        else: return position, move ,move_made

# to check if any player won
def did_win(gameDisplay,position,PATH):
    for i in position:
        coin_home = 0
        for j in position[i][1:]:  #to remove the first element which is None
        # I do not need to check for individual colors as I will call this function
        # after every move so that once 4 coins of any player is in home, the game ends.
            if i == 'red' and j == PATH[58]:
                coin_home +=1
            elif i == 'yellow' and j == PATH[70]:
                coin_home += 1
            elif i == 'green' and j == PATH[76]:
                coin_home += 1
            elif i== 'blue' and j == PATH[64]:
                coin_home += 1
        if coin_home == 4:
            gameDisplay.fill(BLACK)
            message_to_screen(color = WHITE, msg = "Player " + i + " won.",where_text = (0,0))
            return i
    return -1

def message_to_screen(color,msg = 'PLAYER',where_text = (100,22)):
    textSurface = medfont.render(msg, True, color)
    textRect = textSurface.get_rect()
    textRect.center = where_text[0], where_text[1]
    gameDisplay.blit(textSurface, textRect)

def playercontrol(player):
    if player == 'red':
        message_to_screen(color = GREEN)
        return 'green'
    elif player == 'green':
        message_to_screen(color = YELLOW)
        return 'yellow'
    elif player == 'blue':
        message_to_screen(color = RED )
        return 'red'
    elif player == 'yellow':
        message_to_screen(color = BLUE)
        return 'blue'
def gameloop():
    gameOver = False
    gameExit = False
    while not gameExit:
        #if gameOver == True: ##########come back later - replay options
            #pass
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = gameExit = True
        PATH, coin_position = game_initialize()
        player = 'red'
        message_to_screen(color = RED )
        move = roll()
        while not gameOver:
            gameDisplay.blit(image,(0,45))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = gameExit = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    player = playercontrol(player)
                    move = roll()
                elif event.type == pygame.MOUSEBUTTONUP:
                        coin_selected = detect_coin(pygame.mouse.get_pos(),coin_position)
                        if coin_selected and coin_selected[0][0] == player:
                            #print move,coin_selected,coin_position
                            player_change = True
                            prev_move = move
                            coin_position, move, move_made = coin_move(coin_position,coin_selected,move,PATH)
                            if did_win(gameDisplay,coin_position,PATH) != -1:
                                gameOver = True
                            if prev_move == 6:  player_change = False
                            else: player_change = move_made
                        else:
                            player_change = False
                        if player_change:
                            player = playercontrol(player)

            drawcoins(coin_position,PATH)
            pygame.display.update()
            clock.tick(FPS)

############################# GAME EXIT ###############################################################
gameloop()
pygame.quit()
exit()

################################ CITATIONS ############################################################


