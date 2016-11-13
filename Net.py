import numpy as np

def nonlin(x, deriv=False):
    if(deriv==True):
        return (x*(1-x))
    return 1/(1+np.exp(-x))


board = []
colTracker = []
players=[]

def addPiece(column, p):
    count=0
    winner=0
    if(colTracker[column]<0):
        winner=p*-1
        return winner
    else:
        board[colTracker[column]][column]=p
        colTracker[column]-=1
        for i in range(0,6): # check column win
    		if((count > 0) and (board[i][column] != p)): # reset counter if not consecutive
    			count = 0
    		if(board[i][column] == p):
    			count += 1

    		if count == 4: # WIN CONDITION MET
    			winner = p
    			return winner
    	count = 0 # reset
    	return winner
        #Win Check
    '''
	count = 0
	for i in range(5,-1,-1): # iterate rows to add piece

		if(board[i][column] == 0): # checking for empty row to place
			board[i][column] = p

			for j in range(0, 7): # check row win
				if((count > 0) and (board[i][j] != p)): # reset counter if not consecutive
					count = 0
				if(board[i][j] == p):
					count += 1

				if(count == 4): # WIN CONDITION MET
					winner = p
					print winner,' won'
					return
			break
		elif(i == 0): # LOSE CONDITION MET
			winner = -1*p
			return
	count = 0 # reset
	# check win conditions
	for i in range(0,6): # check column win
		if((count > 0) and (board[i][column] != p)): # reset counter if not consecutive
			count = 0
		if(board[i][column] == p):
			count += 1

		if count == 4: # WIN CONDITION MET
			winner = p
			print winner,' won'
			return
	count = 0 # reset
	return
    '''

def runPlayer(playerNum):
    out=(nonlin(np.dot(flatten(6,7,board), players[playerNum])))
    m=out[0]
    index=0
    for x in range(1,7):
        if(out[x]>m):
            m=out[x]
            index=x
    return index

def play(playerA,playerB):
    player=1
    w=0
    while(w==0):
        #for p in range(6):
        	#print board[p]
        if(player==1):
            w=addPiece(runPlayer(playerA), player)
        else:
            w=addPiece(runPlayer(playerA), player)
    	player *= -1

    if(w==1):
        return playerA
    else:
        return playerB

def run():
    tournament()


def flatten(x,y,arr):
    out=[]
    for a in range(x):
        for b in range(y):
            out.append(board[a][b])
    return out

def tournament():
    contestants=[]
    for k in range(len(players)):
        contestants.append(k)
    winners = []
    while (len(contestants)>2):
        winners = []
        for k in range(len(contestants)/2):
            winners.append(play(contestants[k], contestants[len(contestants)-k-1]))
        contestants=winners
    return winners

def init():
    numIn=42
    numOut=7
    numPlayers=8
    np.random.seed(0)
    for i in range(0,6): # rows
    	board.append([])
    	for j in range(0,7): # columns
    		board[i].append(0)
    for i in range(7):
        colTracker.append(5)
    for k in range(numPlayers):
        players.append(2*np.random.random((numIn,numOut))-1)

if __name__ == '__main__':
    init()
    run()
