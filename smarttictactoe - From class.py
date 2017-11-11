import random

board = "1 2 3 4 5 6 7 8 9".split()
player = 0
def trytoWin(b,p):
    for i in range(len(board)):
        if board[i] != 'X' and board[i] != 'O':
            board[i] = 'O'
            if getResult(board) == 2:
                board[i] = str(i+1)
                return i+1
            board[i] = str(i+1)
    return -1
def canweLose(b,p):
    for i in range(len(board)):
        if board[i] != 'X' and board[i] != 'O':
            board[i] = 'X'
            if getResult(board) == 2:
                board[i] = str(i+1)
                return i+1
            board[i] = str(i+1)
    return -1        
def randommove(b,p):
    return random.randint(1,9)
def center(b,p):
    if b[4] == '5':
        return 5
    return -1
def myAI(b,p):
    strategies = [trytoWin,canweLose,center,randommove]
    for strat in strategies:
        val = strat(b,p)
        if val != -1:
            return val

def printBoard(b):
    print b[0]+"|"+b[1]+"|"+b[2]
    print "-------"
    print b[3]+"|"+b[4]+"|"+b[5]
    print "-------"
    print b[6]+"|"+b[7]+"|"+b[8]

def getResult(b):
    if b[0] == b[1] == b[2]:
        return 2
    if b[3] == b[4] == b[5]:
        return 2
    if b[6] == b[7] == b[8]:
        return 2
    if b[0] == b[3] == b[6]:
        return 2
    if b[1] == b[4] == b[7]:
        return 2
    if b[2] == b[5] == b[8]:
        return 2
    if b[0] == b[4] == b[8]:
        return 2
    if b[2] == b[4] == b[6]:
        return 2
    if b.count('X') + b.count('O') == 9:
        return 1
    return 0

def getMove(board,p):
    if p == 0:
        val = int(raw_input("Enter your move "))
    else:
        val = myAI(board,p)#random.randint(1,9)
    return val

def isMoveValid(board,m):
    if m >= 1 and m<=9:
        if board[m-1] != 'X' and board[m-1] != 'O':
            return True
    return False
def makeMove(board,m,player):
    marks = ['X','O']
    board[m-1] = marks[player]
def saveGame(b,p):
    gm = open("tictac.gm","w")
    gm.write(str(p)+"\n")
    for elem in b:
        gm.write(elem+"\n")
    gm.close()

def loadGame(b):
    gm = open("tictac.gm")
    pl = int(gm.readline().strip())
    for i in range(len(b)):
        b[i] = gm.readline().strip()
    return pl


#player = loadGame(board)    
# print the board
printBoard(board)
result = getResult(board)
while result == 0:
#get move from user
    m = getMove(board,player)
    #check if move is valid
    #as long as move is invalid retry

    while(not isMoveValid(board,m)):
        if m == 0:
            saveGame(board,player)
        m = getMove(board,player)
    
    #Make the move
    makeMove(board,m,player)
    
    #Check if there is a result
    #exit if there is a result
    result = getResult(board)
    #Switch players
    if result == 0:
        player = (player + 1) % 2
    printBoard(board)
    print ""

if result == 1:
    print "It is a Tie"
else:
    print "Player ",player+1," Won"






    
