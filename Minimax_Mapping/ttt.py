import operator
import csv

bestMoves = []

def score(board,playerNum,depth):
    #Diagnonal Check
    if (board[0] == board[8] & board[0]==board[4]) | (board[2] == board[6] & board[2]==board[4]) :
      if board[4]==playerNum:
          return 10 - depth
      elif board[4]==(-1*playerNum):
          return depth - 10

    #Horizontal check
    n=0
    while n<9:
      if board[n]==board[n+1] & board[n+1]==board[n+2]:
        if board[n]==playerNum:
            return 10 - depth
        elif board[n]==(-1*playerNum):
            return depth - 10
      n=n+3
      #Vertical check
    n=0
    while n<3:
        if board[n]==board[n+3] & board[n+3]==board[n+6]:
          if board[n]==playerNum:
              return 10 - depth
          elif board[n]==(-1*playerNum):
              return depth - 10
        n=n+1
    return 0


def moveCheck(board,playerNum,index):
    if board[index]==0:
        return True
    else:
        return False

def moveMake(board,playerNum,index):
    board[index]=playerNum
    return board

def Maximize(board,playerNum,depth):
    currentScore = score(board, playerNum, depth)
    print board,playerNum,depth
    if currentScore!=0:
        return currentScore
    #Otherwise find largest of the rest
    else:
        possibleMoves = {}
        for index in range(9):
            boardCopy =  board
            #print index
            if moveCheck(boardCopy,playerNum,index):
                possibleMoves[index] = Maximize( moveMake(boardCopy,playerNum,index) , playerNum*-1 , depth+1)

        currentBest = max(possibleMoves.iteritems(), key=operator.itemgetter(1))[0]
        board = [i * playerNum for i in board]
        bestMoves.append((board,currentBest))
        return possibleMoves[currentBest]

def start():
    b=[0,0,0,0,0,0,0,0,0]
    Maximize(b,1,0)

def writeOut():
    writer = csv.writer(open('ttt.csv','w+'))
    for entry in bestMoves:

        writer.writerow(",".join(entry[0])+str(entry[1]))

start()
writeOut()
