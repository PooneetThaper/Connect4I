import numpy as np
import csv
import time

'''
    Hello, Welcome to Connect4I
    This project uses neural nets and genetic algorithms to ATTEMPT to teach the computer to play Connect$
    In order to run this project, simply navigate to the folder with this file and use the command line command:
    "python Net.py"

    It will show you the board and prompt you when it is your turn. You will be playing as playerB
    and your peices on the board will be "-1" (because we wanted the nets to recognize you as the enemy)
    If you would like to see the computer play againsts itself, please go down to the demo function and
    change the default value of the manual parameter to 0.
'''

def nonlin(x):
    #this function is used as the activation function of the neurons (sigmoid)
    return 1/(1+np.exp(-x))


board = []
colTracker = []
players=[]

def addPiece(column, p):
    #the addpeice checks to see if the game has been won or lost
    #note an illegal move (ex: a move in a full row) is an automatic loss
	count=0
	winner=0
	if(colTracker[column]<0): # LOSE CONDITION MET
		winner=p*-1
		#print winner
		return winner
	else: # ADD PIECE TO COLUMN
		board[colTracker[column]][column]=p

		for j in range(0, 7): # check row win
			if((count > 0) and (board[colTracker[column]][j] != p)): # reset counter if not consecutive
				count = 0
			if(board[colTracker[column]][j] == p):
				count += 1

				if(count == 4): # WIN CONDITION MET
					winner = p
					return winner
		count = 0 # reset

		# check diagonal win
		# diagonal L down to R
		# left half
		i = colTracker[column]
		#print i
		j = column
		#print j
		while((i > 0) and (j > 0)):
			if(board[i][j] == p):
				count += 1
			else:
				if(count > 0):
					count = 0
			if(count == 4): # WIN CONDITION MET
				winner = p
				return winner
			i -= 1
			j -= 1
		# right half
		i = colTracker[column]
		j = column
		while((i < 5) and (j < 6)):
			if(board[i][j] == p):
				count += 1
			else:
				if(count > 0):
					count = 0
			if(count == 4): # WIN CONDITION MET
				winner = p
				return winner
			i += 1
			j += 1
		count = 0
		# diagonal R down to L
		# left half
		i = colTracker[column]
		j = column
		while((i < 5) and (j > 0)):
			if(board[i][j] == p):
				count += 1
			else:
				if(count > 0):
					count = 0
			if(count == 4): # WIN CONDITION MET
				winner = p
				return winner
			i += 1
			j -= 1
		# right half
		i = colTracker[column]
		j = column
		while((i > 0) and (j < 6)):
			if(board[i][j] == p):
				count += 1
			else:
				if(count > 0):
					count = 0
			if(count == 4): # WIN CONDITION MET
				winner = p
				return winner
			i -= 1
			j += 1
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
		#print 'Current Winner ',winner
		return winner

def runPlayer(playerNum,playerVal):
    #Getting the weights of the player in question
    currentPlayer=players[playerNum];
    #Getting the output by using matrix multiplication on a flattened version of the board
    out1=(nonlin(np.dot(flatten(6,7,board,playerVal), currentPlayer[0])))
    out2=(nonlin(np.dot(out1,currentPlayer[1])))
    out=(nonlin(np.dot(out2,currentPlayer[2])))
    #print out
    #Finding the max of the seven outputs to decide on the next move
    m=out[0]
    index=0
    for x in range(1,7):
        if(out[x]>m):
            m=out[x]
            index=x
    #Returning move
    return index

def play(playerA,playerB):
    #controls the game between two players
    reset()
    player=1
    w=0
    out=-1
    #while there is no winner, switches between the players
    while(w==0):
        if(player==1):
            w=addPiece(runPlayer(playerA,1), player)
        else:
            w=addPiece(runPlayer(playerA,-1), player)
    	player *= -1
    if(w==1):
        out=playerA
    else:
        out=playerB
    return out

def train():
    for x in range(1000000):
        #tournament is run to have the eight players compete and return the two winners
        k=tournament()
        #gen is used to create the next generation from the winners from the tournament
        gen(k[0],k[1])
        if (x%100==0):
            print(x)
        if(x%1000==999):
            #periodically, the results are printed out and saved to a CSV
            out=flattenPlayer(7)
            csvOut=[]
            for i in range(len(out)):
                csvOut.append(str(float(out[i])))
            with open("out2.csv","w+") as f:
                spamwriter = csv.writer(f, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)

                spamwriter.writerow(csvOut)
            for row in players[0]:
                print "\t".join(csvOut)


def gen(playerA,playerB):
        #given the two starting players, gen creates 6 players based of of the original 2
        #random crossbreeding and mutations are done for variations
    	d = []
    	d.append(flattenPlayer(playerA))
    	d.append(flattenPlayer(playerB))
        d.append(d[0][:])
        d.append(d[1][:])
    	a = np.random.random(len(d[0]))
    	for l in range(len(d[0])):
    		if(a[l] > 0.5):
    			temp = d[2][l]
    			d[2][l] = d[3][l]
    			d[3][l] = temp*(2*np.random.random(1)-1)
        for l in range(len(d)):
            d.append(d[l][:])
        for j in range(2):
    		a = np.random.random(len(d[0]))
    		for l in range(len(d[0])):
    			if(a[l] > 0.5):
    				temp = d[len(d)/2+j][l]
    				d[len(d)/2+j][l]=d[len(d)-j-1][l]
    				d[len(d)-j-1][l]=temp*(2*np.random.random(1)-1)
        for l in range(len(players)):
            players[l]=deflattenPlayer(d[l])

def flattenPlayer(playerNum):
    #flattens the three layers of the players into one long array
    input=[]

    curr=flatten(42,20,players[playerNum][0])
    for k in curr:
        input.append(k)

    curr=flatten(20,20,players[playerNum][1])
    for k in curr:
        input.append(k)

    curr=flatten(20,7,players[playerNum][1])
    for k in curr:
        input.append(k)

    return input

def deflattenPlayer(arr):
    #reconstructs the players from a flattened player
    out=[]

    temp=[]
    for i in range(840):
        temp.append(arr[i])
    curr=deflatten(42,20,temp)
    out.append(curr)

    temp=[]
    for i in range(840,1240):
        temp.append(arr[i])
    curr=deflatten(20,20,temp)
    out.append(curr)

    temp=[]
    for i in range(1240,1380):
        temp.append(arr[i])
    curr=deflatten(20,7,temp)
    out.append(curr)

    return out;

def deflatten(x,y,arr):
    #turns a single dimensional array into two dimensional array of dimensions x and y
    #(reverses flatten)
    out=[]
    for a in range(x):
        o=[]
        for b in range(y):
            o.append(arr[(a*y)+b])
        out.append(o)
    return out

def flatten(x,y,arr,pval=1):
    #turns a turns a two dimensional array of dimensions x and y into a
    #single dimensional array for more efficient operations
    out=[]
    for a in range(x):
        for b in range(y):
            out.append(pval*arr[a][b])
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
    #print winners
    return winners

def reset():
    for i in range(7):
        colTracker[i]=5
    for row in range(6):
        for col in range(7):
            board[row][col]=0

def demo(playerA,playerB,manual=1):
    reset()
    player=1
    w=0
    out=-1
    while(w==0):
        for p in range(1,8):
            out=[]

        for p in range(6):
        	print board[p][0],"\t",board[p][1],"\t",board[p][2],"\t",board[p][3],"\t",board[p][4],"\t",board[p][5],"\t",board[p][6]
        time.sleep(1)
        print "\n"
        if(player==1):
            w=addPiece(runPlayer(playerA,1), player)
        else:
            if(manual==1):
                print "Choose your column (1-7)"
                r=raw_input()
                w=addPiece(int(r)-1, player)
                print "\n"
            else:
                #To watch the computer play itself,
                #change manual default in function declaration to 0
                w=addPiece(runPlayer(playerB,-1), player)
    	player *= -1


    for p in range(6):
        print board[p][0],"\t",board[p][1],"\t",board[p][2],"\t",board[p][3],"\t",board[p][4],"\t",board[p][5],"\t",board[p][6]

    if(w==1):
        print "playerA won"
    else:
        print "playerB won"

def run():
    #Uncomment train in order to train
    #train()
    #Uncomment demo in order to run the model
    demo(7,7)
    print('done')

def init():
    #initial parameters
    numIn=42
    numOut=7
    numPlayers=8
    #setting up board
    for i in range(0,6): # rows
    	board.append([])
    	for j in range(0,7): # columns
    		board[i].append(0)
    #setting up tracking for each column (for illegal move checking)
    for i in range(7):
        colTracker.append(5)
    #creating random weights for neural nets
    for k in range(numPlayers-1):
        # numPlayers-1 are created while the last one (pretrained) is loaded from the csv
        p=[]
        p.append(2*np.random.random((numIn,20))-1)
        p.append(2*np.random.random((20,20))-1)
        p.append(2*np.random.random((20,numOut))-1)
        players.append(p);
        #players are stored in the player global array

    r=[]
    with open("out2.csv","r") as f:
        spamreader = csv.reader(f, delimiter=',', quotechar='|')
        for row in spamreader:
            for item in row:
                #print item;
                r.append(float(item))
    players.append(deflattenPlayer(r))


if __name__ == '__main__':
    init()
    run()
