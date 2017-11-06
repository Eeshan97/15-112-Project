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

#######################################################################################################

############################## CONSTANTS ##############################################################
DISPLAY_HEIGHT = 800
DISPLAY_WIDTH = 1200
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
#######################################################################################################
def mainmenu():
    gameDisplay = pygame.display.set_mode(DISPLAY_WIDTH,DISPLAY_HEIGHT)
    pygame.display.set_caption('LUDO - Main Menu')

############################# GAME EXIT ###############################################################
pygame.quit()
exit()

################################ CITATIONS ############################################################

# Main Menu Image = <https://www.codester.com/static/uploads/items/3366/icon.png>
