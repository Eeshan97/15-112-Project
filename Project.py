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
import os
import copy
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
COIN_RADIUS = SQUARE_SIZE/3
gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))
pygame.display.set_caption('LUDO - Main Menu')
image = pygame.image.load('ludo.jpg')
pygame.display.set_icon(image)
clock = pygame.time.Clock()
FPS = 7
no_of_six = 0
medfont = pygame.font.SysFont("comicsansms",50)
smallfont = pygame.font.SysFont("comicsansms", 40)
PATH = chalk_path.PATH(SQUARE_SIZE)
SAFE_ZONE = [2,15,28,40]  # Pawns cannot be captured here
RED_HOME = [(PATH[4][0],PATH[10][1]),(PATH[4][0],PATH[8][1]),(PATH[3][0],PATH[9][1]),(PATH[5][0],PATH[9][1])]
BLUE_HOME = [(PATH[23][0],PATH[18][1]),(PATH[23][0],PATH[16][1]),(PATH[22][0],PATH[17][1]),(PATH[24][0],PATH[17][1])]
YELLOW_HOME = [(PATH[23][0],PATH[35][1]),(PATH[23][0],PATH[37][1]),(PATH[22][0],PATH[36][1]),(PATH[24][0],PATH[36][1])]
GREEN_HOME = [(PATH[4][0],PATH[43][1]),(PATH[4][0],PATH[41][1]),(PATH[3][0],PATH[42][1]),(PATH[5][0],PATH[42][1])]
for i in range(1,len(PATH)):
        PATH[i] = (PATH[i][0] + SQUARE_SIZE/2 , PATH[i][1] + SQUARE_SIZE/2)
spritesheet = [] # to store the images of dice
for i in range(1,7):
    spritesheet.append(pygame.image.load('dice (' + str(i)+').png'))
print 'done loading'
#######################################################################################################
def roll(i=0):  #rolling the dice
    global no_of_six
    if no_of_six < 3:
        options = [1,2,3,4,5,6]
    else:
        options = [1,2,3,4,5]
    dice = random.choice(options)
    if dice==6:  no_of_six += 1
    else: no_of_six = 0
    while i <12:
        pygame.draw.rect(gameDisplay,BLACK,(300,0,DISPLAY_WIDTH-300,50))
        temp = random.choice(options)
        gameDisplay.blit(spritesheet[temp-1],(300 + (i%6)*45,0))
        message_to_screen(color = WHITE, msg = str(temp), where_text = (DISPLAY_WIDTH-100,22) )
        i += 1
        clock.tick(4*FPS)
        pygame.display.update()
    pygame.draw.rect(gameDisplay,BLACK,(500,0,DISPLAY_WIDTH-500,50))
    gameDisplay.blit(spritesheet[dice-1],(500,0))
    message_to_screen(color = WHITE, msg = str(dice), where_text = (DISPLAY_WIDTH-100,22) )
    return dice

# this brings back the coins back to the original position
# this function also empties the path
def game_initialize(gameDisplay):
    #intro(gameDisplay)
    position = {'red':[None],'blue':[None],'yellow':[None],'green':[None]}
      #RED COINS
    for i in RED_HOME:
        position['red'].append(i)
    #BLUE COINS
    for i in BLUE_HOME:
        position['blue'].append(i)
    #YELLOW COINS
    for i in YELLOW_HOME:
        position['yellow'].append(i)
    #GREEN COINS
    for i in GREEN_HOME:
        position['green'].append(i)
    AI_list = intro(gameDisplay)
    gameDisplay.fill(BLACK)
    return (PATH,position,AI_list)

def intro(gameDisplay):
    intro_end = False
    AI_list = []
    temp = []
    while not intro_end:
        gameDisplay.fill(BLACK)
        message_to_screen(WHITE,msg = "Press P to play.",where_text = (350,100))
        message_to_screen(WHITE,msg = "You can choose multiple players.",where_text = (350,270),small = True)
        message_to_screen(WHITE,msg = "Just press multiple keys.",where_text = (350,340),small = True)
        message_to_screen(WHITE,msg = "Press I for instructions.",where_text = (350,200))
        message_to_screen(RED,msg = "Press R to play as Red",where_text = (350,700))
        message_to_screen(BLUE,msg = "Press B to play as Blue",where_text = (350,400))
        message_to_screen(GREEN,msg = "Press G to play as Green",where_text = (350,500))
        message_to_screen(YELLOW,msg = "Press Y to play as Yellow",where_text = (350,600))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    intro_end = True
                if event.key == pygame.K_r and 'red' not in temp:
                    temp.append('red')
                if event.key == pygame.K_g and 'green' not in temp:
                    temp.append('green')
                if event.key == pygame.K_y and 'yellow' not in temp:
                    temp.append('yellow')
                if event.key == pygame.K_b and 'blue' not in temp:
                    temp.append('blue')
                if event.key == pygame.K_i:
                    os.system("Notepad.exe rules.txt")
        pygame.display.update()
        clock.tick(FPS)
    for i in ['blue','green','red','yellow']:
        if i not in temp:
            AI_list.append(i)
    return AI_list


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
def capture(color,start,destination,position,PATH):
    for k in position[color][1:]:
        if k == PATH[destination]:
            return position
    coin_captured = None
    for j in position:
        if j!=color:
            counter = 0
            for k in position[j][1:]:
                counter += 1
                if k==PATH[destination]:
                    coin_captured = (j,counter)
    if coin_captured:
        if coin_captured[0] == 'red':
            home = RED_HOME
        elif coin_captured[0] == 'yellow':
            home = YELLOW_HOME
        elif coin_captured[0] == "green":
            home = GREEN_HOME
        elif coin_captured[0] == "blue":
            home = BLUE_HOME
        for i in home:
            isEmpty = True
            for j in position[coin_captured[0]]:
                if i==j:
                    isEmpty = False
            if isEmpty:
                position[coin_captured[0]][coin_captured[1]] = i
                return position
    return position

def is_coin_present(position,color,destination,coin_number):
        for j in position:
            is_present = False
            for k in position[j][1:]:
                if k == PATH[destination]:
                    is_present = True
            if is_present :
                return (position,False)
        position[color][coin_number] = PATH[destination]
        return (position,True)

def AI(color,position,PATH,move):
    #this is a ruled based AI
    print color,move
    counter_coins_pocket = 0
    which_coins = []
    for i in range(1,5):
        for j in [58,64,70,76]: #home pocket numbers
            if position[color][i] == PATH[j]:
                counter_coins_pocket += 1
            elif i not in which_coins:
                which_coins.append(i)
    if counter_coins_pocket == 3:
        return coin_move(position,[(color,which_coins[0])],move,PATH)
    temp = position.copy()
    for i in which_coins:
        if position[color][i] in PATH:
            temp_position = copy.copy(position)
            temp_position , move , move_made = coin_move(temp_position,[(color,i)],move,PATH,check_roll = False)
            for j in temp_position:
                if j!=color and temp_position[j]!=position[j]:
                    print 'capture'
                    return temp_position,roll(),move_made
    position = temp
    if move == 6:
        for coin_number in which_coins:
            print coin_number
            if position[color][coin_number] not in PATH:
                if color == 'red':
                    position, move_made = is_coin_present(position,color,2,coin_number)
                elif color == 'blue':
                     position, move_made = is_coin_present(position,color,15,coin_number)
                elif color == 'green':
                      position, move_made = is_coin_present(position,color,41,coin_number)
                else:
                    position, move_made = is_coin_present(position,color,28,coin_number)
                if move_made:
                    print 'move six'
                    return position,roll(),move_made
    move_made = False
    no_of_trials = 0
    temp = []
    for i in which_coins:
        if position[color][i] in PATH:
            temp.append(i)
    which_coins = temp
    temp = position.copy()
    for i in which_coins:
        for j in [58,64,70,76]:
            temp_position = copy.copy(position)
            if position[color][i] == PATH[j-move]:
                _ ,_ , move_made = coin_move(temp_position,[(color,i)],move,PATH,check_roll = False)
                if move_made:
                    return temp_position, roll(), move_made
    position = temp
    while not move_made and no_of_trials <10 and which_coins:
        temp_position = copy.copy(position)
        temp_position , _ , move_made = coin_move(temp_position,[(color,random.choice(which_coins))],move,PATH,check_roll = False)
        no_of_trials += 1
    if move_made:
        print "random move made"
        return temp_position, roll(), move_made
    print "turn passed"
    position = temp
    return position,roll(),True


def coin_move(position,coin_selected,move,PATH, check_roll = True):
        color = coin_selected[0][0]
        coin_number = coin_selected[0][1]
        move_made = True
        did_coin_start = detect_square_number(PATH,position[color][coin_number])
        if not did_coin_start:
            if move == 6:
                if color == 'red':
                  position, move_made = is_coin_present(position,color,2,coin_number)
                elif color == 'blue':
                   position, move_made = is_coin_present(position,color,15,coin_number)
                elif color == 'green':
                    position, move_made = is_coin_present(position,color,41,coin_number)
                else:
                    position, move_made = is_coin_present(position,color,28,coin_number)
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
                #temp = position
                move = did_coin_start+move-52
                if is_valid_move(color,did_coin_start,53,position,PATH):
                    if is_valid_move(color,1,move,position,PATH):
                        position = capture(color,1,move,position,PATH)
                        #if temp == position:
                         #position[color][coin_number] = PATH[did_coin_start + move]
                else: move_made = False
            else:
                destination = (did_coin_start + move)
                temp = position
                if is_valid_move(color,did_coin_start,destination,position,PATH):
                    position = capture(color,did_coin_start,destination,position,PATH)
                    if temp == position:
                        position[color][coin_number] = PATH[did_coin_start + move]
                else: move_made = False
        if move_made and check_roll:
            print color,coin_number,move
            return position, roll(),move_made
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
            message_to_screen(color = WHITE, msg = "Player " + i + " won.",where_text = (350,350))
            time.sleep(10)
            return i
    return -1

def message_to_screen(color,msg = 'PLAYER',where_text = (100,22),small = False):
    if not small :textSurface = medfont.render(msg, True, color)
    else: textSurface = smallfont.render(msg, True, color)
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
        PATH, coin_position, AI_list = game_initialize(gameDisplay)
        player = 'red'
        message_to_screen(color = RED )
        move = roll(12)
        while not gameOver:
            gameDisplay.blit(image,(0,45))
            for event in (pygame.event.get() + [1]):
                if event != 1 and event.type == pygame.QUIT:
                    gameOver = gameExit = True
                elif event != 1 and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    player = playercontrol(player)
                    move = roll()
                elif (event != 1 and event.type == pygame.MOUSEBUTTONUP) or player in AI_list:
                        is_AI_playing = player in AI_list
                        if not is_AI_playing:
                            coin_selected = detect_coin(pygame.mouse.get_pos(),coin_position)
                        else:
                            coin_selected = [[player]]
                        if coin_selected and coin_selected[0][0] == player:
                            player_change = True
                            prev_move = move
                            if not is_AI_playing:
                               coin_position, move, move_made = coin_move(coin_position,coin_selected,move,PATH)
                            else:
                                coin_position, move, move_made = AI(player,coin_position,PATH,move)
                            if did_win(gameDisplay,coin_position,PATH) != -1:
                                gameOver = True
                            if prev_move == 6:  player_change = False
                            else: player_change = move_made
                        else:
                            player_change = False
                        if player_change:
                            player = playercontrol(player)

            if not gameOver: drawcoins(coin_position,PATH)
            pygame.display.update()
            clock.tick(FPS)

############################# GAME EXIT ###############################################################
gameloop()
pygame.quit()
exit()

################################ CITATIONS ############################################################


